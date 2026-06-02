from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.sql_draft_service import SQLDraftService
from app.services.sql_safety_service import review_sql


class SQLExecutionService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
        warehouse_repository: WarehouseRepository,
    ) -> None:
        self._warehouse_repository = warehouse_repository
        self._draft_service = SQLDraftService(metadata_repository, warehouse_repository)

    def execute_draft(
        self,
        question: str,
        table_limit: int = 3,
        field_limit: int = 20,
        fields_per_table: int = 12,
        limit: int = 100,
    ) -> dict[str, Any]:
        draft = self._draft_service.draft_select(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
            limit=limit,
        )
        sql = draft.get("sql")
        review = draft.get("review") or {}
        if not sql or not review.get("allowed"):
            return {
                "question": question,
                "draft": draft,
                "executed": False,
                "result": None,
                "warnings": [*draft.get("warnings", []), "Draft SQL was not executable."],
            }

        # Re-review the exact SQL at the execution boundary.
        execution_review = review_sql(sql)
        if not execution_review.allowed:
            return {
                "question": question,
                "draft": draft,
                "execution_review": asdict(execution_review),
                "executed": False,
                "result": None,
                "warnings": [*draft.get("warnings", []), "SQL was blocked at execution boundary."],
            }

        result = self._warehouse_repository.execute_select(sql, max_rows=max(1, min(limit, 1000)))
        return {
            "question": question,
            "draft": draft,
            "execution_review": asdict(execution_review),
            "executed": True,
            "result": result,
            "warnings": draft.get("warnings", []),
        }
