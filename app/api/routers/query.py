from __future__ import annotations

import pymysql
from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.core.request_context import get_request_id
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.services.query_planning_service import QueryPlanningService
from app.services.sql_draft_service import SQLDraftService


router = APIRouter(prefix="/api/query", tags=["query"])


def _planning_service() -> QueryPlanningService:
    settings = get_settings()
    return QueryPlanningService(
        metadata_repository=MetadataRepository(settings.metadata_db),
        warehouse_repository=WarehouseRepository(settings.warehouse_db),
    )


def _sql_draft_service() -> SQLDraftService:
    settings = get_settings()
    return SQLDraftService(
        metadata_repository=MetadataRepository(settings.metadata_db),
        warehouse_repository=WarehouseRepository(settings.warehouse_db),
    )


@router.get("/prepare")
def prepare_query(
    question: str = Query(min_length=1, description="Natural language question"),
    table_limit: int = Query(default=3, ge=1, le=10),
    field_limit: int = Query(default=20, ge=1, le=100),
    fields_per_table: int = Query(default=12, ge=1, le=50),
) -> dict[str, object]:
    try:
        data = _planning_service().prepare(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": data,
    }


@router.get("/draft-sql")
def draft_sql(
    question: str = Query(min_length=1, description="Natural language question"),
    table_limit: int = Query(default=3, ge=1, le=10),
    field_limit: int = Query(default=20, ge=1, le=100),
    fields_per_table: int = Query(default=12, ge=1, le=50),
    limit: int = Query(default=100, ge=1, le=1000),
) -> dict[str, object]:
    try:
        data = _sql_draft_service().draft_select(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": data,
    }
