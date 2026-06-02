from __future__ import annotations

from typing import Any

from app.repositories.metadata_repository import MetadataRepository
from app.services.metadata_retrieval_service import MetadataRetrievalService


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _compact_dict(row: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: row.get(key) for key in keys if _text(row.get(key))}


def _field_line(field: dict[str, Any]) -> str:
    parts = [
        _text(field.get("field_name")) or "<no_physical_field>",
        _text(field.get("field_display_name")),
    ]
    if _text(field.get("data_type")):
        parts.append(f"type={_text(field.get('data_type'))}")
    if _text(field.get("business_definition")):
        parts.append(f"definition={_text(field.get('business_definition'))}")
    if _text(field.get("formula")):
        parts.append(f"formula={_text(field.get('formula'))}")
    if _text(field.get("usage_notes")):
        parts.append(f"notes={_text(field.get('usage_notes'))}")
    return " | ".join(part for part in parts if part)


def _dedupe_fields(fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique_fields = []
    for field in fields:
        key = (_text(field.get("field_name")).lower(), _text(field.get("field_display_name")))
        if key in seen:
            continue
        seen.add(key)
        unique_fields.append(field)
    return unique_fields


class MetadataContextService:
    def __init__(self, repository: MetadataRepository) -> None:
        self._retrieval = MetadataRetrievalService(repository)

    def build_context(
        self,
        question: str,
        table_limit: int = 3,
        field_limit: int = 20,
        fields_per_table: int = 10,
    ) -> dict[str, Any]:
        retrieval = self._retrieval.retrieve(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )

        tables = []
        warnings: list[str] = []
        prompt_sections = [f"User question: {question}", "Candidate warehouse metadata:"]

        for table_context in retrieval["candidate_tables"]:
            table = table_context["table"]
            fields = _dedupe_fields(table_context["fields"])
            table_name = _text(table.get("table_name"))
            table_display_name = _text(table.get("table_display_name"))
            table_id = _text(table.get("table_id"))

            if not table_name:
                warnings.append(f"Candidate table {table_id} has no physical table name in metadata.")

            compact_fields = [
                _compact_dict(
                    field,
                    [
                        "field_id",
                        "field_name",
                        "field_display_name",
                        "data_type",
                        "business_definition",
                        "formula",
                        "usage_notes",
                        "metric_type",
                        "channel",
                    ],
                )
                for field in fields
            ]

            tables.append(
                {
                    "table_id": table_id,
                    "table_name": table_name,
                    "table_display_name": table_display_name,
                    "score": table_context["score"],
                    "grain": table.get("grain"),
                    "primary_key": table.get("primary_key"),
                    "description": table.get("description"),
                    "usage_notes": table.get("usage_notes"),
                    "fields": compact_fields,
                }
            )

            prompt_sections.append(
                f"- table_id={table_id}; table_name={table_name or '<missing>'}; "
                f"display_name={table_display_name}; score={table_context['score']}"
            )
            if _text(table.get("grain")):
                prompt_sections.append(f"  grain: {_text(table.get('grain'))}")
            if _text(table.get("primary_key")):
                prompt_sections.append(f"  primary_key: {_text(table.get('primary_key'))}")
            if _text(table.get("description")):
                prompt_sections.append(f"  description: {_text(table.get('description'))}")
            if _text(table.get("usage_notes")):
                prompt_sections.append(f"  table_notes: {_text(table.get('usage_notes'))}")
            prompt_sections.append("  fields:")
            for field in fields:
                prompt_sections.append(f"    - {_field_line(field)}")

        return {
            "question": question,
            "terms": retrieval["terms"],
            "tables": tables,
            "candidate_fields": retrieval["candidate_fields"],
            "prompt_context": "\n".join(prompt_sections),
            "warnings": warnings,
        }
