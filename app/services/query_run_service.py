from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime
from dataclasses import asdict
import re
from typing import Any

from app.clients.llm import OpenAICompatibleClient
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.llm_sql_generation_service import LLMSQLGenerationService
from app.services.query_planning_service import QueryPlanningService
from app.services.sql_execution_service import SQLExecutionService
from app.services.sql_safety_service import review_sql


_BACKTICK_IDENTIFIER_PATTERN = re.compile(r"`([^`]+)`")


class QueryRunService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
        warehouse_repository: WarehouseRepository,
        llm_client: OpenAICompatibleClient | None = None,
    ) -> None:
        self._metadata_repository = metadata_repository
        self._warehouse_repository = warehouse_repository
        self._executor = SQLExecutionService(metadata_repository, warehouse_repository)
        self._llm_client = llm_client

    def run(
        self,
        question: str,
        table_limit: int = 1,
        field_limit: int = 20,
        fields_per_table: int = 20,
        limit: int = 100,
        mode: str = "draft",
    ) -> dict[str, Any]:
        run_id = str(uuid.uuid4())
        started = time.perf_counter()
        started_at = datetime.now(UTC).isoformat()

        execution_started = time.perf_counter()
        if mode == "draft":
            execution = self._executor.execute_draft(
                question=question,
                table_limit=table_limit,
                field_limit=field_limit,
                fields_per_table=fields_per_table,
                limit=limit,
                stop_after_first_ready=True,
            )
        elif mode == "llm_draft":
            execution = self._execute_llm_draft(
                question=question,
                table_limit=table_limit,
                field_limit=field_limit,
                fields_per_table=fields_per_table,
                limit=limit,
            )
        else:
            raise ValueError(f"Unsupported query run mode: {mode}")
        execution_elapsed_ms = round((time.perf_counter() - execution_started) * 1000, 2)
        total_elapsed_ms = round((time.perf_counter() - started) * 1000, 2)

        draft = execution.get("draft") or {}
        plan = draft.get("plan") or {}
        selected_table = plan.get("selected_table") or {}
        result = execution.get("result") or {"columns": [], "rows": [], "row_count": 0, "elapsed_ms": 0}

        if execution.get("executed"):
            answer_status = "ok"
        elif draft.get("ready_to_execute") is False:
            answer_status = "not_ready"
        else:
            answer_status = "blocked"

        return {
            "run_id": run_id,
            "question": question,
            "mode": mode,
            "started_at": started_at,
            "answer_status": answer_status,
            "sql": draft.get("sql"),
            "selected_table": {
                "table_id": selected_table.get("table_id"),
                "table_name": selected_table.get("table_name"),
                "table_display_name": selected_table.get("table_display_name"),
            }
            if selected_table
            else None,
            "columns": result.get("columns", []),
            "rows": result.get("rows", []),
            "row_count": result.get("row_count", 0),
            "elapsed_ms": result.get("elapsed_ms", 0),
            "warnings": execution.get("warnings", []),
            "trace": {
                "run_id": run_id,
                "started_at": started_at,
                "finished_at": datetime.now(UTC).isoformat(),
                "total_elapsed_ms": total_elapsed_ms,
                "steps": [
                    {
                        "step_id": "draft_and_execute",
                        "status": "ok" if execution.get("executed") else "blocked",
                        "elapsed_ms": execution_elapsed_ms,
                    },
                    {
                        "step_id": "sql_execution",
                        "status": "ok" if execution.get("executed") else "skipped",
                        "elapsed_ms": result.get("elapsed_ms", 0),
                    },
                ],
                "draft_ready_to_execute": draft.get("ready_to_execute"),
                "draft_review": draft.get("review"),
                "execution_review": execution.get("execution_review"),
                "executed": execution.get("executed", False),
                "llm": draft.get("llm"),
            },
        }

    def _execute_llm_draft(
        self,
        question: str,
        table_limit: int,
        field_limit: int,
        fields_per_table: int,
        limit: int,
    ) -> dict[str, Any]:
        if self._llm_client is None:
            return {
                "question": question,
                "draft": {
                    "ready_to_execute": False,
                    "review": None,
                    "sql": None,
                    "llm": None,
                    "warnings": ["LLM client is not configured."],
                },
                "executed": False,
                "result": None,
                "warnings": ["LLM client is not configured."],
            }

        planner = QueryPlanningService(self._metadata_repository, self._warehouse_repository)
        generator = LLMSQLGenerationService(planner, self._llm_client)
        draft = generator.generate(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
            limit=limit,
        )
        sql = draft.get("sql")
        if not sql:
            return {
                "question": question,
                "draft": draft,
                "executed": False,
                "result": None,
                "warnings": [*draft.get("warnings", []), "LLM did not produce executable SQL."],
            }

        review = review_sql(sql)
        draft["review"] = asdict(review)
        draft["ready_to_execute"] = review.allowed
        if not review.allowed:
            return {
                "question": question,
                "draft": draft,
                "execution_review": asdict(review),
                "executed": False,
                "result": None,
                "warnings": [*draft.get("warnings", []), "LLM SQL was blocked by safety review."],
            }

        schema_error = _validate_llm_sql_identifiers(sql, draft)
        if schema_error:
            return {
                "question": question,
                "draft": draft,
                "execution_review": asdict(review),
                "executed": False,
                "result": None,
                "warnings": [*draft.get("warnings", []), schema_error],
            }

        result = self._warehouse_repository.execute_select(sql, max_rows=max(1, min(limit, 1000)))
        return {
            "question": question,
            "draft": draft,
            "execution_review": asdict(review),
            "executed": True,
            "result": result,
            "warnings": draft.get("warnings", []),
        }


def _validate_llm_sql_identifiers(sql: str, draft: dict[str, Any]) -> str | None:
    plan = draft.get("plan") or {}
    selected_table = plan.get("selected_table") or {}
    table_name = selected_table.get("table_name")
    allowed = {table_name}
    allowed.update(
        column.get("column_name")
        for column in selected_table.get("warehouse_columns", [])
        if column.get("column_name")
    )
    identifiers = set(_BACKTICK_IDENTIFIER_PATTERN.findall(sql))
    if not identifiers:
        return "LLM SQL must quote table and column identifiers with backticks."
    disallowed = sorted(identifier for identifier in identifiers if identifier not in allowed)
    if disallowed:
        return f"LLM SQL referenced identifiers outside selected schema: {', '.join(disallowed)}"
    return None
