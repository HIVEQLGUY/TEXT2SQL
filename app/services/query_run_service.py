from __future__ import annotations

from typing import Any

from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.sql_execution_service import SQLExecutionService


class QueryRunService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
        warehouse_repository: WarehouseRepository,
    ) -> None:
        self._executor = SQLExecutionService(metadata_repository, warehouse_repository)

    def run(
        self,
        question: str,
        table_limit: int = 1,
        field_limit: int = 20,
        fields_per_table: int = 20,
        limit: int = 100,
    ) -> dict[str, Any]:
        execution = self._executor.execute_draft(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
            limit=limit,
            stop_after_first_ready=True,
        )
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
            "question": question,
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
                "draft_ready_to_execute": draft.get("ready_to_execute"),
                "draft_review": draft.get("review"),
                "execution_review": execution.get("execution_review"),
                "executed": execution.get("executed", False),
            },
        }
