from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any

from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.metadata_retrieval_service import extract_retrieval_terms
from app.services.query_planning_service import QueryPlanningService
from app.services.sql_safety_service import review_sql


_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _quote_identifier(identifier: str) -> str:
    if not _IDENTIFIER_PATTERN.fullmatch(identifier):
        raise ValueError(f"Unsafe SQL identifier: {identifier}")
    return f"`{identifier}`"


def _field_relevance(field: dict[str, Any], terms: list[str]) -> float:
    haystack = " ".join(
        str(value or "").lower()
        for value in (
            field.get("field_name"),
            field.get("field_display_name"),
            field.get("business_definition"),
            field.get("formula"),
        )
    )
    score = 0.0
    for term in terms:
        if term.lower() in haystack:
            score += 1.0 + min(len(term), 8) / 8
    return score


def _unique_columns(fields: list[dict[str, Any]], question: str, maximum: int = 12) -> list[str]:
    terms = extract_retrieval_terms(question)
    ranked_fields = sorted(
        fields,
        key=lambda field: (-_field_relevance(field, terms), str(field.get("field_display_name") or "")),
    )
    columns = []

    for term in terms:
        if len(term) < 2:
            continue
        term_lower = term.lower()
        best_field = next(
            (
                field
                for field in ranked_fields
                if term_lower
                in " ".join(
                    str(value or "").lower()
                    for value in (
                        field.get("field_name"),
                        field.get("field_display_name"),
                        field.get("business_definition"),
                        field.get("formula"),
                    )
                )
            ),
            None,
        )
        if best_field:
            column = best_field.get("warehouse_column", {}).get("column_name") or best_field.get("field_name")
            if column and column not in columns:
                columns.append(column)
        if len(columns) >= maximum:
            return columns

    for field in ranked_fields:
        column = field.get("warehouse_column", {}).get("column_name") or field.get("field_name")
        if column and column not in columns:
            columns.append(column)
        if len(columns) >= maximum:
            break
    return columns


def _warehouse_column_fields(columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "field_name": column.get("column_name"),
            "field_display_name": column.get("column_comment"),
            "data_type": column.get("data_type"),
            "warehouse_column": column,
        }
        for column in columns
    ]


class SQLDraftService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
        warehouse_repository: WarehouseRepository,
    ) -> None:
        self._planner = QueryPlanningService(metadata_repository, warehouse_repository)

    def draft_select(
        self,
        question: str,
        table_limit: int = 3,
        field_limit: int = 20,
        fields_per_table: int = 12,
        limit: int = 100,
    ) -> dict[str, Any]:
        plan = self._planner.prepare(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )
        selected_table = plan["selected_table"]
        if not selected_table:
            return {
                "question": question,
                "plan": plan,
                "sql": None,
                "review": None,
                "ready_to_execute": False,
                "warnings": [*plan["warnings"], "No SQL-ready table was found."],
            }

        table_name = selected_table["table_name"]
        column_candidates = [
            *selected_table["matched_fields"],
            *_warehouse_column_fields(selected_table.get("warehouse_columns", [])),
        ]
        columns = _unique_columns(column_candidates, question)
        if not columns:
            return {
                "question": question,
                "plan": plan,
                "sql": None,
                "review": None,
                "ready_to_execute": False,
                "warnings": [*plan["warnings"], "No SQL-ready columns were found."],
            }

        safe_limit = max(1, min(limit, 1000))
        select_list = ", ".join(_quote_identifier(column) for column in columns)
        sql = f"SELECT {select_list} FROM {_quote_identifier(table_name)} LIMIT {safe_limit}"
        review = review_sql(sql)

        warnings = list(plan["warnings"])
        warehouse_table = selected_table.get("warehouse_table") or {}
        if warehouse_table.get("table_rows") == 0:
            warnings.append(f"Physical table row estimate is 0; statistics may be stale: {table_name}")

        return {
            "question": question,
            "plan": plan,
            "sql": sql,
            "review": asdict(review),
            "ready_to_execute": review.allowed,
            "warnings": warnings,
        }
