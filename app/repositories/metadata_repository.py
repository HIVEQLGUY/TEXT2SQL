from __future__ import annotations

from typing import Any

from app.clients.mysql import mysql_connection
from app.core.config import DatabaseSettings


def _clamp_limit(limit: int, maximum: int = 200) -> int:
    return max(1, min(limit, maximum))


def _like_pattern(query: str) -> str:
    return f"%{query}%"


def _normalized_terms(terms: list[str], maximum: int = 12) -> list[str]:
    normalized: list[str] = []
    for term in terms:
        term = term.strip()
        if term and term not in normalized:
            normalized.append(term)
        if len(normalized) >= maximum:
            break
    return normalized


class MetadataRepository:
    """Read adapter for the upstream warehouse metadata dictionaries."""

    def __init__(self, db_settings: DatabaseSettings) -> None:
        self._db_settings = db_settings

    def get_summary(self) -> dict[str, Any]:
        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS c FROM table_dictionary")
                table_count = cursor.fetchone()["c"]

                cursor.execute("SELECT COUNT(*) AS c FROM metric_dictionary")
                field_count = cursor.fetchone()["c"]

                cursor.execute(
                    """
                    SELECT COUNT(*) AS c
                    FROM metric_dictionary m
                    JOIN table_dictionary t ON m.ssscb = t.bbs
                    """
                )
                associated_field_count = cursor.fetchone()["c"]

                cursor.execute(
                    """
                    SELECT COUNT(*) AS c
                    FROM metric_dictionary
                    WHERE ssscb IS NULL OR TRIM(ssscb) = ''
                    """
                )
                unassigned_field_count = cursor.fetchone()["c"]

        return {
            "table_count": table_count,
            "field_count": field_count,
            "associated_field_count": associated_field_count,
            "unassigned_field_count": unassigned_field_count,
            "association": {
                "table_id_column": "table_dictionary.bbs",
                "field_table_id_column": "metric_dictionary.ssscb",
            },
        }

    def search_tables(self, query: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        conditions: list[str] = []
        params: list[Any] = []
        if query:
            pattern = _like_pattern(query.strip())
            conditions.append(
                """
                (
                    bywm LIKE %s
                    OR bzwm LIKE %s
                    OR zty LIKE %s
                    OR ywdx LIKE %s
                    OR bms LIKE %s
                )
                """
            )
            params.extend([pattern] * 5)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(_clamp_limit(limit))

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        bbs AS table_id,
                        bywm AS table_name,
                        bzwm AS table_display_name,
                        zty AS subject_area,
                        ywdx AS business_object,
                        bld AS grain,
                        zj AS primary_key,
                        syzycj AS usage_notes,
                        bms AS description,
                        gxpl AS update_frequency,
                        jrly AS source,
                        szfx AS analysis_area,
                        bhzd AS field_ids
                    FROM table_dictionary
                    {where_clause}
                    ORDER BY table_display_name, table_name
                    LIMIT %s
                    """,
                    params,
                )
                return list(cursor.fetchall())

    def search_tables_by_terms(self, terms: list[str], limit: int = 100) -> list[dict[str, Any]]:
        normalized_terms = _normalized_terms(terms)
        if not normalized_terms:
            return []

        searchable_columns = ["bywm", "bzwm", "zty", "ywdx", "bms"]
        term_conditions = [
            "(" + " OR ".join(f"{column} LIKE %s" for column in searchable_columns) + ")"
            for _ in normalized_terms
        ]
        params: list[Any] = []
        for term in normalized_terms:
            params.extend([_like_pattern(term)] * len(searchable_columns))
        params.append(_clamp_limit(limit))

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        bbs AS table_id,
                        bywm AS table_name,
                        bzwm AS table_display_name,
                        zty AS subject_area,
                        ywdx AS business_object,
                        bld AS grain,
                        zj AS primary_key,
                        syzycj AS usage_notes,
                        bms AS description,
                        gxpl AS update_frequency,
                        jrly AS source,
                        szfx AS analysis_area,
                        bhzd AS field_ids
                    FROM table_dictionary
                    WHERE {" OR ".join(term_conditions)}
                    ORDER BY table_display_name, table_name
                    LIMIT %s
                    """,
                    params,
                )
                return list(cursor.fetchall())

    def search_fields(
        self,
        query: str | None = None,
        table_id: str | None = None,
        table_name: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        conditions: list[str] = []
        params: list[Any] = []

        if table_id:
            conditions.append("m.ssscb = %s")
            params.append(table_id.strip())

        if table_name:
            conditions.append("t.bywm = %s")
            params.append(table_name.strip())

        if query:
            pattern = _like_pattern(query.strip())
            conditions.append(
                """
                (
                    m.zdywmc LIKE %s
                    OR m.zdzwmc LIKE %s
                    OR m.ywdy LIKE %s
                    OR m.jsgs LIKE %s
                    OR m.syzysx LIKE %s
                    OR t.bywm LIKE %s
                    OR t.bzwm LIKE %s
                )
                """
            )
            params.extend([pattern] * 7)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(_clamp_limit(limit))

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        m.zdbs AS field_id,
                        m.zdywmc AS field_name,
                        m.zdzwmc AS field_display_name,
                        m.sjlx AS data_type,
                        m.ywdy AS business_definition,
                        m.jsgs AS formula,
                        m.syzysx AS usage_notes,
                        m.zblx AS metric_type,
                        m.glfzb AS parent_metric,
                        m.glzzb AS child_metric,
                        m.ssqd AS channel,
                        m.gmhzdm AS renamed_field_name,
                        m.sjo AS data_owner,
                        m.ywo AS business_owner,
                        m.ssywy AS business_domain,
                        m.zhgxsj AS last_updated_at,
                        m.ssscb AS table_id,
                        t.bywm AS table_name,
                        t.bzwm AS table_display_name
                    FROM metric_dictionary m
                    LEFT JOIN table_dictionary t ON m.ssscb = t.bbs
                    {where_clause}
                    ORDER BY table_display_name, field_display_name, field_name
                    LIMIT %s
                    """,
                    params,
                )
                return list(cursor.fetchall())

    def search_fields_by_terms(self, terms: list[str], limit: int = 200) -> list[dict[str, Any]]:
        normalized_terms = _normalized_terms(terms)
        if not normalized_terms:
            return []

        searchable_columns = [
            "m.zdywmc",
            "m.zdzwmc",
            "m.ywdy",
            "m.jsgs",
            "m.syzysx",
            "t.bywm",
            "t.bzwm",
        ]
        term_conditions = [
            "(" + " OR ".join(f"{column} LIKE %s" for column in searchable_columns) + ")"
            for _ in normalized_terms
        ]
        params: list[Any] = []
        for term in normalized_terms:
            params.extend([_like_pattern(term)] * len(searchable_columns))
        params.append(_clamp_limit(limit, maximum=500))

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        m.zdbs AS field_id,
                        m.zdywmc AS field_name,
                        m.zdzwmc AS field_display_name,
                        m.sjlx AS data_type,
                        m.ywdy AS business_definition,
                        m.jsgs AS formula,
                        m.syzysx AS usage_notes,
                        m.zblx AS metric_type,
                        m.glfzb AS parent_metric,
                        m.glzzb AS child_metric,
                        m.ssqd AS channel,
                        m.gmhzdm AS renamed_field_name,
                        m.sjo AS data_owner,
                        m.ywo AS business_owner,
                        m.ssywy AS business_domain,
                        m.zhgxsj AS last_updated_at,
                        m.ssscb AS table_id,
                        t.bywm AS table_name,
                        t.bzwm AS table_display_name
                    FROM metric_dictionary m
                    LEFT JOIN table_dictionary t ON m.ssscb = t.bbs
                    WHERE {" OR ".join(term_conditions)}
                    ORDER BY table_display_name, field_display_name, field_name
                    LIMIT %s
                    """,
                    params,
                )
                return list(cursor.fetchall())

    def list_fields_for_table_ids(self, table_ids: list[str], limit: int = 500) -> list[dict[str, Any]]:
        normalized_ids = _normalized_terms(table_ids, maximum=50)
        if not normalized_ids:
            return []

        placeholders = ", ".join(["%s"] * len(normalized_ids))
        params: list[Any] = [*normalized_ids, _clamp_limit(limit, maximum=1000)]

        with mysql_connection(self._db_settings) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        m.zdbs AS field_id,
                        m.zdywmc AS field_name,
                        m.zdzwmc AS field_display_name,
                        m.sjlx AS data_type,
                        m.ywdy AS business_definition,
                        m.jsgs AS formula,
                        m.syzysx AS usage_notes,
                        m.zblx AS metric_type,
                        m.glfzb AS parent_metric,
                        m.glzzb AS child_metric,
                        m.ssqd AS channel,
                        m.gmhzdm AS renamed_field_name,
                        m.sjo AS data_owner,
                        m.ywo AS business_owner,
                        m.ssywy AS business_domain,
                        m.zhgxsj AS last_updated_at,
                        m.ssscb AS table_id,
                        t.bywm AS table_name,
                        t.bzwm AS table_display_name
                    FROM metric_dictionary m
                    LEFT JOIN table_dictionary t ON m.ssscb = t.bbs
                    WHERE m.ssscb IN ({placeholders})
                    ORDER BY table_display_name, field_display_name, field_name
                    LIMIT %s
                    """,
                    params,
                )
                return list(cursor.fetchall())
