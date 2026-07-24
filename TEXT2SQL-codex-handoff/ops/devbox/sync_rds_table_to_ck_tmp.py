#!/usr/bin/env python3
"""Copy one old-RDS table into a ClickHouse temporary modeling table.

Source side is read-only. Target side creates a temporary-named ClickHouse table
and inserts rows in batches. Existing non-empty target tables are not appended to
unless --append is explicitly provided.
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
from pathlib import Path
from typing import Any

import pymysql
from pymysql.cursors import DictCursor, SSDictCursor


DEFAULT_ENV = Path(r"C:\Users\24796\Documents\TEXT2SQL\local\credentials\project.env")


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def qi(identifier: str) -> str:
    if "`" in identifier:
        raise ValueError(f"unsafe identifier: {identifier}")
    return f"`{identifier}`"


def ql(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def clickhouse_request(args: argparse.Namespace, sql: str, timeout: int = 300) -> str:
    params = {"database": args.ck_database}
    url = f"http://{args.ck_host}:{args.ck_port}/?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, data=sql.encode("utf-8"), method="POST")
    request.add_header("X-ClickHouse-User", args.ck_user)
    request.add_header("X-ClickHouse-Key", args.ck_password)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


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


def source_columns(conn: pymysql.Connection, database: str, table: str) -> list[dict[str, Any]]:
    with conn.cursor(DictCursor) as cursor:
        cursor.execute(
            """
            SELECT column_name, data_type, column_comment, ordinal_position
            FROM information_schema.columns
            WHERE table_schema=%s AND table_name=%s
            ORDER BY ordinal_position
            """,
            (database, table),
        )
        rows = list(cursor.fetchall())
    if not rows:
        raise RuntimeError(f"source table not found or has no columns: {database}.{table}")
    return [{str(k).lower(): v for k, v in row.items()} for row in rows]


def create_target(args: argparse.Namespace, columns: list[dict[str, Any]]) -> None:
    column_lines = []
    for col in columns:
        name = str(col["column_name"])
        comment = str(col.get("column_comment") or "")
        line = f"  {qi(name)} String DEFAULT ''"
        if comment and "\ufffd" not in comment:
            line += f" COMMENT {ql(comment)}"
        column_lines.append(line)

    ddl = f"""
CREATE TABLE IF NOT EXISTS {qi(args.ck_database)}.{qi(args.ck_table)}
(
{",\n".join(column_lines)}
)
ENGINE = MergeTree
ORDER BY tuple()
COMMENT {ql(args.table_comment)}
"""
    clickhouse_request(args, ddl)


def target_count(args: argparse.Namespace) -> int:
    sql = f"SELECT count() FROM {qi(args.ck_database)}.{qi(args.ck_table)} FORMAT TSV"
    output = clickhouse_request(args, sql)
    return int((output.strip() or "0").split("\t")[0])


def source_count(conn: pymysql.Connection, table: str) -> int:
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT count(*) FROM {qi(table)}")
        return int(cursor.fetchone()[0])


def insert_batch(args: argparse.Namespace, column_names: list[str], rows: Iterable[dict[str, Any]]) -> int:
    payload = []
    count = 0
    for row in rows:
        payload.append(json.dumps({name: json_value(row.get(name)) for name in column_names}, ensure_ascii=False))
        count += 1
    if not payload:
        return 0
    sql = (
        f"INSERT INTO {qi(args.ck_database)}.{qi(args.ck_table)} "
        f"({', '.join(qi(c) for c in column_names)}) FORMAT JSONEachRow\n"
        + "\n".join(payload)
        + "\n"
    )
    clickhouse_request(args, sql, timeout=600)
    return count


def sync_rows(conn: pymysql.Connection, args: argparse.Namespace, column_names: list[str]) -> int:
    select_sql = f"SELECT {', '.join(qi(c) for c in column_names)} FROM {qi(args.source_table)}"
    if args.limit:
        select_sql += f" LIMIT {int(args.limit)}"

    inserted = 0
    with conn.cursor(SSDictCursor) as cursor:
        cursor.execute(select_sql)
        while True:
            rows = cursor.fetchmany(args.batch_size)
            if not rows:
                break
            inserted += insert_batch(args, column_names, rows)
            print(f"inserted_batch={len(rows)} total={inserted}", flush=True)
    return inserted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync an old RDS table to a ClickHouse temporary table.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV))
    parser.add_argument("--source-prefix", default="META_DB")
    parser.add_argument("--source-table", required=True)
    parser.add_argument("--ck-host", default=os.getenv("CLICKHOUSE_HOST", "127.0.0.1"))
    parser.add_argument("--ck-port", default=os.getenv("CLICKHOUSE_HTTP_PORT", "8123"))
    parser.add_argument("--ck-user", default=os.getenv("CLICKHOUSE_USER", "default"))
    parser.add_argument("--ck-password", default=os.getenv("CLICKHOUSE_PASSWORD", ""))
    parser.add_argument("--ck-database", default=os.getenv("CLICKHOUSE_DATABASE", "youmei_sandbox"))
    parser.add_argument("--ck-table", required=True)
    parser.add_argument("--table-comment", default="临时建模测试表，可删除")
    parser.add_argument("--batch-size", type=int, default=5000)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--append", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    env = load_env(Path(args.env_file))
    prefix = args.source_prefix
    source_host = env[f"{prefix}_HOST"]
    source_port = int(env.get(f"{prefix}_PORT", "3306"))
    source_user = env[f"{prefix}_USER"]
    source_password = env[f"{prefix}_PASSWORD"]
    source_database = env[f"{prefix}_NAME"]

    conn = pymysql.connect(
        host=source_host,
        port=source_port,
        user=source_user,
        password=source_password,
        database=source_database,
        charset="utf8mb4",
        autocommit=True,
        connect_timeout=10,
        read_timeout=1200,
        write_timeout=1200,
    )
    try:
        columns = source_columns(conn, source_database, args.source_table)
        column_names = [str(col["column_name"]) for col in columns]
        total_source = source_count(conn, args.source_table)
        print(
            json.dumps(
                {
                    "source": f"{source_host}:{source_port}/{source_database}.{args.source_table}",
                    "target": f"{args.ck_database}.{args.ck_table}",
                    "source_rows": total_source,
                    "source_columns": len(columns),
                    "limit": args.limit or None,
                    "dry_run": args.dry_run,
                },
                ensure_ascii=False,
                indent=2,
            ),
            flush=True,
        )
        if args.dry_run:
            return 0

        create_target(args, columns)
        existing = target_count(args)
        if existing and not args.append:
            raise RuntimeError(
                f"target {args.ck_database}.{args.ck_table} already has {existing} rows; "
                "refusing to append without --append"
            )
        inserted = sync_rows(conn, args, column_names)
        final_count = target_count(args)
        print(json.dumps({"inserted": inserted, "target_rows": final_count}, ensure_ascii=False), flush=True)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
