from __future__ import annotations

import re
from typing import Any

from app.repositories.metadata_repository import MetadataRepository


_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]+")
_STOP_TERMS = {
    "一下",
    "一个",
    "多少",
    "如何",
    "是否",
    "查询",
    "帮我",
    "统计",
    "看看",
    "里面",
    "这个",
    "那个",
    "按照",
    "根据",
    "最近",
    "今天",
    "昨天",
    "明天",
}


def _as_text(value: Any) -> str:
    return "" if value is None else str(value)


def _contains_any(row: dict[str, Any], fields: list[str], term: str) -> bool:
    lowered = term.lower()
    return any(lowered in _as_text(row.get(field)).lower() for field in fields)


def _is_ascii_term(term: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", term))


def extract_retrieval_terms(question: str, max_terms: int = 12) -> list[str]:
    terms: list[str] = []

    def add(term: str) -> None:
        term = term.strip()
        if not term or term in _STOP_TERMS or term in terms:
            return
        terms.append(term)

    add(question)
    for token in _TOKEN_PATTERN.findall(question):
        add(token)
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) > 2:
            for size in (4, 3, 2):
                for start in range(0, len(token) - size + 1):
                    add(token[start : start + size])
                    if len(terms) >= max_terms:
                        return terms[:max_terms]
        if len(terms) >= max_terms:
            return terms[:max_terms]

    return terms[:max_terms]


class MetadataRetrievalService:
    def __init__(self, repository: MetadataRepository) -> None:
        self._repository = repository

    def retrieve(
        self,
        question: str,
        table_limit: int = 5,
        field_limit: int = 20,
        fields_per_table: int = 12,
    ) -> dict[str, Any]:
        terms = extract_retrieval_terms(question)
        table_scores: dict[str, float] = {}
        table_rows: dict[str, dict[str, Any]] = {}
        field_scores: dict[str, float] = {}
        field_rows: dict[str, dict[str, Any]] = {}

        for table in self._repository.search_tables_by_terms(terms, limit=100):
            table_id = table["table_id"]
            table_rows[table_id] = table
            for term in terms:
                if _contains_any(table, ["table_name", "table_display_name"], term):
                    table_scores[table_id] = table_scores.get(table_id, 0.0) + (100.0 if _is_ascii_term(term) else 6.0)
                elif _contains_any(table, ["description", "business_object", "subject_area"], term):
                    table_scores[table_id] = table_scores.get(table_id, 0.0) + 3.0

        for field in self._repository.search_fields_by_terms(terms, limit=300):
            field_id = field["field_id"]
            field_rows[field_id] = field
            for term in terms:
                if _contains_any(field, ["field_name", "field_display_name"], term):
                    field_scores[field_id] = field_scores.get(field_id, 0.0) + 3.0
                elif _contains_any(field, ["business_definition", "formula", "usage_notes"], term):
                    field_scores[field_id] = field_scores.get(field_id, 0.0) + 2.0
                elif _contains_any(field, ["table_name", "table_display_name"], term):
                    field_scores[field_id] = field_scores.get(field_id, 0.0) + 1.0

            table_id = field.get("table_id")
            if table_id:
                table_scores[table_id] = table_scores.get(table_id, 0.0) + max(
                    0.25,
                    min(field_scores.get(field_id, 0.0) * 0.15, 1.0),
                )
                table_rows.setdefault(
                    table_id,
                    {
                        "table_id": table_id,
                        "table_name": field.get("table_name"),
                        "table_display_name": field.get("table_display_name"),
                    },
                )

        ranked_tables = sorted(
            table_rows.values(),
            key=lambda row: (-table_scores.get(row["table_id"], 0.0), _as_text(row.get("table_display_name"))),
        )[:table_limit]

        ranked_fields = sorted(
            field_rows.values(),
            key=lambda row: (-field_scores.get(row["field_id"], 0.0), _as_text(row.get("field_display_name"))),
        )[:field_limit]

        table_contexts = []
        table_field_rows: dict[str, list[dict[str, Any]]] = {}
        ranked_table_ids = [table["table_id"] for table in ranked_tables]
        for field in self._repository.list_fields_for_table_ids(ranked_table_ids, limit=500):
            table_field_rows.setdefault(field["table_id"], []).append(field)

        for table in ranked_tables:
            table_id = table["table_id"]
            matched_fields = [
                field
                for field in ranked_fields
                if field.get("table_id") == table_id
            ][:fields_per_table]

            if len(matched_fields) < min(fields_per_table, 5):
                table_fields = table_field_rows.get(table_id, [])
                existing_ids = {field["field_id"] for field in matched_fields}
                for field in table_fields:
                    if field["field_id"] not in existing_ids:
                        matched_fields.append(field)
                    if len(matched_fields) >= fields_per_table:
                        break

            table_contexts.append(
                {
                    "table": table,
                    "score": round(table_scores.get(table_id, 0.0), 3),
                    "fields": matched_fields,
                }
            )

        return {
            "question": question,
            "terms": terms,
            "candidate_tables": table_contexts,
            "candidate_fields": ranked_fields,
        }
