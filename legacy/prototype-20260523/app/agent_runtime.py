from __future__ import annotations

import re
import time
from typing import Any


def answer_from_metadata(question: str, metadata: dict[str, Any], guidance: list[dict[str, str]]) -> dict[str, Any]:
    started = time.perf_counter()
    q = question.strip().lower()
    tables = metadata["tables"]

    if any(word in q for word in ("表", "table", "schema", "元数据", "字段", "column")):
        return {
            "mode": "metadata",
            "message": f"当前数据库 {metadata['database']} 有 {metadata['table_count']} 张表。你可以在左侧元数据区查看表和字段。",
            "suggestions": guidance[:12],
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        }

    matched_tables = []
    for table in tables:
        table_text = " ".join(
            [table["name"], table["comment"], *[column["name"] for column in table["columns"]], *[column["comment"] for column in table["columns"]]]
        ).lower()
        if any(token and token in table_text for token in re.split(r"\s+|，|,|。", q)):
            matched_tables.append(table)

    if matched_tables:
        suggestions = []
        for table in matched_tables[:5]:
            fields = ", ".join(column["name"] for column in table["columns"][:8])
            suggestions.append(
                {
                    "table": table["name"],
                    "fields": fields,
                    "sample_sql": f"SELECT {fields} FROM {table['name']} LIMIT 50",
                }
            )
        return {
            "mode": "analysis_plan",
            "message": "我找到了可能相关的表。为了安全起步，建议先用下方样例 SQL 做字段验证，再扩展成聚合分析。",
            "suggestions": suggestions,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        }

    return {
        "mode": "needs_sql",
        "message": "当前本地测试台还没有接入大模型 API，不能稳定地把复杂自然语言直接转成 SQL。你可以先让我在 Codex 里生成 SQL，或在网页中粘贴 SQL 进行审查和执行。",
        "suggestions": guidance[:8],
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
    }
