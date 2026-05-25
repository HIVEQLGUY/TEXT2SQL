from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

from app.config import DatabaseConfig, ROOT


sys.path.insert(0, str(ROOT / ".codex_deps"))

import pymysql
from pymysql.cursors import DictCursor


def connect(config: DatabaseConfig):
    return pymysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database,
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30,
        charset="utf8mb4",
        cursorclass=DictCursor,
    )


def test_connection(config: DatabaseConfig) -> dict[str, Any]:
    started = time.perf_counter()
    with connect(config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE() AS database_name, VERSION() AS version, CURRENT_USER() AS user_name")
            row = cursor.fetchone()
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "ok": True,
        "elapsed_ms": elapsed_ms,
        "database_name": row["database_name"],
        "version": row["version"],
        "current_user": row["user_name"],
        "config": config.safe_info,
    }


def fetch_all(config: DatabaseConfig, sql: str) -> tuple[list[dict[str, Any]], float]:
    started = time.perf_counter()
    with connect(config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return rows, elapsed_ms
