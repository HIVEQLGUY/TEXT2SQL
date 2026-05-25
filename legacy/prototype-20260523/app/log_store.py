from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from app.config import ROOT


RUNTIME_DIR = ROOT / ".runtime"
DB_PATH = RUNTIME_DIR / "text2sql_runs.sqlite3"


def init_store() -> None:
    RUNTIME_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS run_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                database_name TEXT NOT NULL,
                question TEXT NOT NULL,
                sql_text TEXT,
                review_allowed INTEGER NOT NULL,
                hard_blocks_json TEXT NOT NULL,
                risks_json TEXT NOT NULL,
                status TEXT NOT NULL,
                timings_json TEXT NOT NULL,
                row_count INTEGER NOT NULL DEFAULT 0,
                result_preview_json TEXT,
                error_message TEXT
            )
            """
        )


def save_run(
    *,
    database_name: str,
    question: str,
    sql_text: str | None,
    review_allowed: bool,
    hard_blocks: list[str],
    risks: list[str],
    status: str,
    timings: dict[str, Any],
    row_count: int = 0,
    result_preview: list[dict[str, Any]] | None = None,
    error_message: str | None = None,
) -> int:
    init_store()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO run_logs (
                database_name,
                question,
                sql_text,
                review_allowed,
                hard_blocks_json,
                risks_json,
                status,
                timings_json,
                row_count,
                result_preview_json,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                database_name,
                question,
                sql_text,
                1 if review_allowed else 0,
                json.dumps(hard_blocks, ensure_ascii=False),
                json.dumps(risks, ensure_ascii=False),
                status,
                json.dumps(timings, ensure_ascii=False),
                row_count,
                json.dumps(result_preview or [], ensure_ascii=False, default=str),
                error_message,
            ),
        )
        return int(cursor.lastrowid)


def list_runs(limit: int = 50) -> list[dict[str, Any]]:
    init_store()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT *
            FROM run_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["review_allowed"] = bool(item["review_allowed"])
        item["hard_blocks"] = json.loads(item.pop("hard_blocks_json"))
        item["risks"] = json.loads(item.pop("risks_json"))
        item["timings"] = json.loads(item.pop("timings_json"))
        item["result_preview"] = json.loads(item.pop("result_preview_json") or "[]")
        result.append(item)
    return result
