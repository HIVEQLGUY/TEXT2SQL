from __future__ import annotations

import time
from typing import Any

from app.clients.mysql import mysql_connection
from app.core.config import DatabaseSettings


class WarehouseRepository:
    def __init__(self, db_settings: DatabaseSettings) -> None:
        self._db_settings = db_settings
        self._schema_cache: dict[str, dict[str, Any]] = {}

    def get_table(self, table_name: str) -> dict[str, Any] | None:
        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        TABLE_NAME AS table_name,
                        TABLE_ROWS AS table_rows,
                        TABLE_COMMENT AS table_comment
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = %s
                    """,
                    (table_name,),
                )
                return cursor.fetchone()

    def list_columns(self, table_name: str) -> list[dict[str, Any]]:
        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        COLUMN_NAME AS column_name,
                        DATA_TYPE AS data_type,
                        COLUMN_TYPE AS column_type,
                        IS_NULLABLE AS is_nullable,
                        COLUMN_KEY AS column_key,
                        COLUMN_COMMENT AS column_comment,
                        ORDINAL_POSITION AS ordinal_position
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION
                    """,
                    (table_name,),
                )
                return list(cursor.fetchall())

    def get_schema_snapshot(self, table_name: str) -> dict[str, Any]:
        if table_name in self._schema_cache:
            return self._schema_cache[table_name]

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        TABLE_NAME AS table_name,
                        TABLE_ROWS AS table_rows,
                        TABLE_COMMENT AS table_comment
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = %s
                    """,
                    (table_name,),
                )
                table = cursor.fetchone()

                cursor.execute(
                    """
                    SELECT
                        COLUMN_NAME AS column_name,
                        DATA_TYPE AS data_type,
                        COLUMN_TYPE AS column_type,
                        IS_NULLABLE AS is_nullable,
                        COLUMN_KEY AS column_key,
                        COLUMN_COMMENT AS column_comment,
                        ORDINAL_POSITION AS ordinal_position
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION
                    """,
                    (table_name,),
                )
                columns = list(cursor.fetchall())

        snapshot = {"table": table, "columns": columns}
        self._schema_cache[table_name] = snapshot
        return snapshot

    def execute_select(self, sql: str, max_rows: int = 1000) -> dict[str, Any]:
        started = time.perf_counter()
        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = list(cursor.fetchmany(max_rows))
                columns = [description[0] for description in cursor.description or []]

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "elapsed_ms": elapsed_ms,
        }
