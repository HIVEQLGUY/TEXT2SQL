from __future__ import annotations

import re
from typing import Any

from app.clients.llm import OpenAICompatibleClient
from app.services.metadata_retrieval_service import extract_retrieval_terms
from app.services.query_planning_service import QueryPlanningService
from app.services.sql_draft_service import _unique_columns


_CODE_BLOCK_PATTERN = re.compile(r"```(?:sql)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def _extract_sql(content: str) -> str:
    match = _CODE_BLOCK_PATTERN.search(content)
    sql = match.group(1) if match else content
    sql = sql.strip()
    if sql.lower().startswith("sql\n"):
        sql = sql[4:].strip()
    return sql.rstrip(";").strip()


def _field_relevance(field: dict[str, Any], terms: list[str]) -> float:
    column = field.get("warehouse_column", {})
    haystack = " ".join(
        str(value or "").lower()
        for value in (
            field.get("field_name"),
            field.get("field_display_name"),
            field.get("business_definition"),
            field.get("formula"),
            column.get("column_name"),
            column.get("column_comment"),
        )
    )
    score = 0.0
    for term in terms:
        if term.lower() in haystack:
            score += 1.0 + min(len(term), 8) / 8
    return score


class LLMSQLGenerationService:
    def __init__(
        self,
        planner: QueryPlanningService,
        llm_client: OpenAICompatibleClient,
    ) -> None:
        self._planner = planner
        self._llm_client = llm_client

    def generate(
        self,
        question: str,
        table_limit: int = 1,
        field_limit: int = 20,
        fields_per_table: int = 20,
        limit: int = 100,
    ) -> dict[str, Any]:
        plan = self._planner.prepare(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
            stop_after_first_ready=True,
        )
        selected_table = plan.get("selected_table")
        if not selected_table:
            return {
                "question": question,
                "plan": plan,
                "sql": None,
                "ready_to_execute": False,
                "warnings": [*plan.get("warnings", []), "No SQL-ready table was found for LLM generation."],
                "llm": None,
            }

        terms = extract_retrieval_terms(question)
        ranked_fields = sorted(
            selected_table.get("matched_fields", []),
            key=lambda field: (-_field_relevance(field, terms), str(field.get("field_display_name") or "")),
        )
        schema_lines = []
        for field in ranked_fields:
            column = field.get("warehouse_column", {})
            column_name = column.get("column_name") or field.get("field_name")
            if not column_name:
                continue
            schema_lines.append(
                f"- {column_name}: {field.get('field_display_name') or column.get('column_comment') or ''} "
                f"({column.get('data_type') or field.get('data_type') or 'unknown'})"
            )
        recommended_columns = _unique_columns(ranked_fields, question, maximum=8)

        table_name = selected_table["table_name"]
        prompt = (
            "You are a MySQL Text2SQL generator. Generate exactly one SQL query.\n"
            "Rules:\n"
            "- Return SQL only, no explanation.\n"
            "- Only SELECT queries are allowed.\n"
            "- Use only the provided table and columns.\n"
            "- Do not use SELECT *.\n"
            f"- Always include LIMIT {max(1, min(limit, 1000))}.\n"
            "- Quote identifiers with backticks.\n\n"
            f"User question:\n{question}\n\n"
            f"Allowed table:\n{table_name} ({selected_table.get('table_display_name')})\n\n"
            "Recommended columns to cover the question first:\n"
            + ", ".join(f"`{column}`" for column in recommended_columns)
            + "\n\n"
            "Allowed columns:\n"
            + "\n".join(schema_lines)
        )
        messages = [
            {"role": "system", "content": "You generate safe MySQL SELECT statements for analytics."},
            {"role": "user", "content": prompt},
        ]
        llm_response = self._llm_client.chat(messages=messages, temperature=0.0)
        sql = _extract_sql(llm_response["content"])

        return {
            "question": question,
            "plan": plan,
            "sql": sql,
            "ready_to_execute": bool(sql),
            "warnings": plan.get("warnings", []),
            "llm": {
                "model": llm_response.get("model"),
                "usage": llm_response.get("usage"),
                "raw_content": llm_response.get("content"),
            },
        }
