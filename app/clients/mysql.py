from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from app.core.config import DatabaseSettings


@contextmanager
def mysql_connection(settings: DatabaseSettings) -> Iterator[Connection]:
    kwargs: dict[str, Any] = {
        "host": settings.host,
        "port": settings.port,
        "user": settings.user,
        "password": settings.password,
        "database": settings.database,
        "connect_timeout": settings.connect_timeout,
        "read_timeout": settings.read_timeout,
        "write_timeout": settings.write_timeout,
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
        "autocommit": True,
    }
    if settings.mysql_get_server_public_key:
        kwargs["server_public_key"] = None

    conn = pymysql.connect(**kwargs)
    try:
        yield conn
    finally:
        conn.close()


def ping_database(settings: DatabaseSettings) -> dict[str, Any]:
    started = time.perf_counter()
    with mysql_connection(settings) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT DATABASE() AS database_name, "
                "CURRENT_USER() AS current_user_name, VERSION() AS version, 1 AS ok"
            )
            row = cursor.fetchone()
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "ok": True,
        "elapsed_ms": elapsed_ms,
        "database_name": row["database_name"],
        "current_user": row["current_user_name"],
        "version": row["version"],
    }
