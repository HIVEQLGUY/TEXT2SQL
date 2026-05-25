from __future__ import annotations

import time
from typing import Any

from app.config import DatabaseConfig
from app.db import connect


def load_metadata(config: DatabaseConfig) -> dict[str, Any]:
    started = time.perf_counter()
    with connect(config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    TABLE_NAME AS name,
                    TABLE_COMMENT AS comment,
                    TABLE_ROWS AS rows_count,
                    ENGINE AS engine
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
                """,
                (config.database,),
            )
            tables = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    TABLE_NAME AS table_name,
                    COLUMN_NAME AS name,
                    ORDINAL_POSITION AS ordinal_position,
                    COLUMN_TYPE AS column_type,
                    IS_NULLABLE AS is_nullable,
                    COLUMN_KEY AS column_key,
                    COLUMN_DEFAULT AS column_default,
                    COLUMN_COMMENT AS column_comment
                FROM information_schema.columns
                WHERE table_schema = %s
                ORDER BY table_name, ordinal_position
                """,
                (config.database,),
            )
            columns = cursor.fetchall()

    table_map: dict[str, dict[str, Any]] = {}
    for table in tables:
        table_map[table["name"]] = {
            "name": table["name"],
            "comment": table["comment"] or "",
            "rows": table["rows_count"],
            "engine": table["engine"],
            "columns": [],
        }

    for column in columns:
        table_name = column["table_name"]
        if table_name not in table_map:
            continue
        table_map[table_name]["columns"].append(
            {
                "name": column["name"],
                "type": column["column_type"],
                "nullable": column["is_nullable"],
                "key": column["column_key"],
                "default": column["column_default"],
                "comment": column["column_comment"] or "",
            }
        )

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "database": config.database,
        "elapsed_ms": elapsed_ms,
        "table_count": len(table_map),
        "tables": list(table_map.values()),
    }


def build_analysis_guidance(metadata: dict[str, Any]) -> list[dict[str, str]]:
    guidance: list[dict[str, str]] = []
    for table in metadata["tables"]:
        names = {column["name"].lower() for column in table["columns"]}
        suggestions: list[str] = []
        if any(name in names for name in ("created_at", "create_time", "gmt_create", "order_time", "pay_time")):
            suggestions.append("time trend")
        if any("amount" in name or "price" in name or "money" in name or "fee" in name for name in names):
            suggestions.append("amount summary")
        if any("status" in name or "state" in name for name in names):
            suggestions.append("status distribution")
        if any("user" in name or "customer" in name or "member" in name for name in names):
            suggestions.append("customer analysis")
        if suggestions:
            guidance.append(
                {
                    "table": table["name"],
                    "comment": table["comment"],
                    "ideas": ", ".join(sorted(set(suggestions))),
                }
            )
    return guidance
