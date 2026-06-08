from __future__ import annotations

from typing import Any

from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.metadata_context_service import MetadataContextService


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _column_lookup(columns: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {column["column_name"].lower(): column for column in columns}


class QueryPlanningService:
    def __init__(
        self,
        metadata_repository: MetadataRepository,
        warehouse_repository: WarehouseRepository,
    ) -> None:
        self._metadata_context = MetadataContextService(metadata_repository)
        self._warehouse_repository = warehouse_repository

    def prepare(
        self,
        question: str,
        table_limit: int = 3,
        field_limit: int = 20,
        fields_per_table: int = 12,
        stop_after_first_ready: bool = False,
    ) -> dict[str, Any]:
        metadata_context = self._metadata_context.build_context(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )

        prepared_tables = []
        warnings = list(metadata_context["warnings"])

        for table in metadata_context["tables"]:
            table_name = _text(table.get("table_name"))
            if not table_name:
                prepared_tables.append(
                    {
                        **table,
                        "warehouse_table": None,
                        "warehouse_columns": [],
                        "matched_fields": [],
                        "unmatched_fields": table.get("fields", []),
                        "ready_for_sql": False,
                    }
                )
                continue

            snapshot = self._warehouse_repository.get_schema_snapshot(table_name)
            warehouse_table = snapshot["table"]
            warehouse_columns = snapshot["columns"]
            if warehouse_table is None:
                warnings.append(f"Physical table not found in warehouse DB: {table_name}")

            lookup = _column_lookup(warehouse_columns)
            matched_fields = []
            unmatched_fields = []
            for field in table.get("fields", []):
                field_name = _text(field.get("field_name"))
                column = lookup.get(field_name.lower()) if field_name else None
                if column:
                    matched_fields.append(
                        {
                            **field,
                            "warehouse_column": column,
                        }
                    )
                else:
                    unmatched_fields.append(field)

            if warehouse_table:
                matched_column_names = {
                    field.get("warehouse_column", {}).get("column_name")
                    for field in matched_fields
                    if field.get("warehouse_column", {}).get("column_name")
                }
                matched_fields.extend(
                    {
                        "field_id": None,
                        "field_name": column["column_name"],
                        "field_display_name": column.get("column_comment"),
                        "data_type": column.get("data_type"),
                        "warehouse_column": column,
                    }
                    for column in warehouse_columns
                    if column["column_name"] not in matched_column_names
                )

            prepared_tables.append(
                {
                    **table,
                    "warehouse_table": warehouse_table,
                    "warehouse_columns": warehouse_columns,
                    "matched_fields": matched_fields,
                    "unmatched_fields": unmatched_fields,
                    "ready_for_sql": bool(warehouse_table and matched_fields),
                }
            )
            if stop_after_first_ready and prepared_tables[-1]["ready_for_sql"]:
                break

        ready_tables = [table for table in prepared_tables if table["ready_for_sql"]]
        return {
            "question": question,
            "metadata_context": metadata_context,
            "tables": prepared_tables,
            "ready_for_sql": bool(ready_tables),
            "selected_table": ready_tables[0] if ready_tables else None,
            "warnings": warnings,
        }
