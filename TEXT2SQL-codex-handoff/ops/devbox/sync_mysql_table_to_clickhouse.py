#!/usr/bin/env python3
"""Sync a bounded MySQL-compatible table sample into ClickHouse.

This is intended for local modeling tests: read-only on the source side,
append-only on the ClickHouse side unless the caller explicitly runs cleanup SQL.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pymysql
from pymysql.cursors import DictCursor


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def qi(identifier: str) -> str:
    if "`" in identifier:
        raise ValueError(f"unsafe identifier: {identifier}")
    return f"`{identifier}`"


def split_table(value: str) -> tuple[str | None, str]:
    parts = value.split(".", 1)
    if len(parts) == 1:
        return None, parts[0]
    return parts[0], parts[1]


def json_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ")
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", errors="replace")
    return str(value)


def clickhouse_request(args: argparse.Namespace, sql: str, timeout: int = 120) -> str:
    params = {"database": args.ck_database}
    url = f"http://{args.ck_host}:{args.ck_port}/?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, data=sql.encode("utf-8"), method="POST")
    request.add_header("X-ClickHouse-User", args.ck_user)
    request.add_header("X-ClickHouse-Key", args.ck_password)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def clickhouse_insert(args: argparse.Namespace, columns: list[str], rows: Iterable[dict[str, Any]]) -> int:
    insert_sql = (
        f"INSERT INTO {qi(args.ck_database)}.{qi(args.ck_table)} "
        f"({', '.join(qi(c) for c in columns)}) FORMAT JSONEachRow\n"
    )
    count = 0
    payload_lines: list[str] = []
    for row in rows:
        payload_lines.append(json.dumps({c: json_value(row.get(c)) for c in columns}, ensure_ascii=False))
        count += 1
    if not payload_lines:
        return 0
    clickhouse_request(args, insert_sql + "\n".join(payload_lines) + "\n", timeout=300)
    return count


def source_columns(conn: pymysql.Connection, database: str, table: str) -> list[str]:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema=%s AND table_name=%s
            ORDER BY ordinal_position
            """,
            (database, table),
        )
        return [row[0] for row in cursor.fetchall()]


def target_columns(args: argparse.Namespace) -> list[str]:
    sql = (
        "SELECT name FROM system.columns "
        f"WHERE database={json.dumps(args.ck_database)} AND table={json.dumps(args.ck_table)} "
        "ORDER BY position FORMAT TSV"
    )
    output = clickhouse_request(args, sql)
    return [line.strip() for line in output.splitlines() if line.strip()]


def resolve_where(
    conn: pymysql.Connection,
    args: argparse.Namespace,
    src_database: str,
    src_table: str,
    src_cols: set[str],
) -> tuple[str, tuple[Any, ...], str]:
    if args.where:
        return f"WHERE {args.where}", (), f"custom where: {args.where}"
    if "dt" not in src_cols:
        return "", (), "no dt column; bounded by LIMIT only"
    with conn.cursor() as cursor:
        cursor.execute(
            f"SELECT max({qi('dt')}) FROM {qi(src_database)}.{qi(src_table)} "
            f"WHERE {qi('dt')} IS NOT NULL AND cast({qi('dt')} AS char) <> ''"
        )
        latest_dt = cursor.fetchone()[0]
    if latest_dt is None:
        return "", (), "dt exists but max(dt) is null; bounded by LIMIT only"
    return f"WHERE {qi('dt')}=%s", (latest_dt,), f"latest dt: {latest_dt}"


def batched_fetch(
    conn: pymysql.Connection,
    sql: str,
    params: tuple[Any, ...],
    batch_size: int,
) -> Iterable[list[dict[str, Any]]]:
    with conn.cursor(DictCursor) as cursor:
        cursor.execute(sql, params)
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield list(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync one MySQL-compatible table sample into ClickHouse.")
    parser.add_argument("--source-host", default=env("SOURCE_DB_HOST", env("SR_HOST", "127.0.0.1")))
    parser.add_argument("--source-port", type=int, default=int(env("SOURCE_DB_PORT", env("SR_PORT", "19030"))))
    parser.add_argument("--source-user", default=env("SOURCE_DB_USER", env("SR_USER", "ro1")))
    parser.add_argument("--source-password", default=env("SOURCE_DB_PASSWORD", env("SR_PASS", "")))
    parser.add_argument("--source-database", default=env("SOURCE_DB_NAME", "cubeappdata"))
    parser.add_argument("--source-table", default="ods_api_dd_sale_order_list_info_du")
    parser.add_argument("--ck-host", default=env("CLICKHOUSE_HOST", "127.0.0.1"))
    parser.add_argument("--ck-port", default=env("CLICKHOUSE_HTTP_PORT", "8123"))
    parser.add_argument("--ck-user", default=env("CLICKHOUSE_USER", "default"))
    parser.add_argument("--ck-password", default=env("CLICKHOUSE_PASSWORD", ""))
    parser.add_argument("--ck-database", default=env("CLICKHOUSE_DATABASE", "youmei_sandbox"))
    parser.add_argument("--ck-table", default="tmp_ods_api_dd_sale_order_list_info_du_model_test")
    parser.add_argument("--where", help="Optional source SQL WHERE expression. Do not include the WHERE keyword.")
    parser.add_argument("--max-rows", type=int, default=10_000)
    parser.add_argument("--batch-size", type=int, default=1_000)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source_password:
        sys.stderr.write("SOURCE_DB_PASSWORD or SR_PASS is required for the source connection.\n")
        return 2

    src_db_from_table, src_table = split_table(args.source_table)
    src_database = src_db_from_table or args.source_database

    conn = pymysql.connect(
        host=args.source_host,
        port=args.source_port,
        user=args.source_user,
        password=args.source_password,
        database=src_database,
        charset="utf8mb4",
        autocommit=True,
        connect_timeout=10,
        read_timeout=600,
        write_timeout=600,
    )
    try:
        src_cols = source_columns(conn, src_database, src_table)
        ck_cols = target_columns(args)
        if not src_cols:
            raise RuntimeError(f"source table not found or has no columns: {src_database}.{src_table}")
        if not ck_cols:
            raise RuntimeError(f"ClickHouse target table not found or has no columns: {args.ck_database}.{args.ck_table}")

        shared_cols = [c for c in ck_cols if c in set(src_cols)]
        missing_in_source = [c for c in ck_cols if c not in set(src_cols)]
        if not shared_cols:
            raise RuntimeError("no shared columns between source and ClickHouse target")

        where_sql, where_params, where_note = resolve_where(conn, args, src_database, src_table, set(src_cols))
        select_sql = (
            f"SELECT {', '.join(qi(c) for c in shared_cols)} "
            f"FROM {qi(src_database)}.{qi(src_table)} {where_sql} "
            f"LIMIT {int(args.max_rows)}"
        )

        print(
            json.dumps(
                {
                    "source": f"{args.source_host}:{args.source_port}/{src_database}.{src_table}",
                    "target": f"{args.ck_database}.{args.ck_table}",
                    "where": where_note,
                    "source_columns": len(src_cols),
                    "target_columns": len(ck_cols),
                    "shared_columns": len(shared_cols),
                    "missing_target_columns_filled_blank": missing_in_source,
                    "max_rows": args.max_rows,
                    "dry_run": args.dry_run,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        if args.dry_run:
            return 0

        inserted = 0
        for batch in batched_fetch(conn, select_sql, where_params, args.batch_size):
            if missing_in_source:
                for row in batch:
                    for col in missing_in_source:
                        row[col] = ""
            inserted += clickhouse_insert(args, ck_cols, batch)
            print(f"inserted_batch={len(batch)} total={inserted}")

        count_sql = (
            f"SELECT count() AS rows, min(dt), max(dt) "
            f"FROM {qi(args.ck_database)}.{qi(args.ck_table)} FORMAT TSV"
        )
        print("clickhouse_validation=" + clickhouse_request(args, count_sql).strip())
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
