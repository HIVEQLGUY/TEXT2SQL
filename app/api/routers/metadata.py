from __future__ import annotations

import pymysql
from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.core.request_context import get_request_id
from app.repositories.metadata_repository import MetadataRepository
from app.services.metadata_context_service import MetadataContextService
from app.services.metadata_retrieval_service import MetadataRetrievalService


router = APIRouter(prefix="/api/metadata", tags=["metadata"])


def _repository() -> MetadataRepository:
    return MetadataRepository(get_settings().metadata_db)


def _retrieval_service() -> MetadataRetrievalService:
    return MetadataRetrievalService(_repository())


def _context_service() -> MetadataContextService:
    return MetadataContextService(_repository())


@router.get("/summary")
def metadata_summary() -> dict[str, object]:
    try:
        data = _repository().get_summary()
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": data,
    }


@router.get("/tables")
def search_tables(
    q: str | None = Query(default=None, description="Keyword for table metadata"),
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, object]:
    try:
        rows = _repository().search_tables(query=q, limit=limit)
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "count": len(rows),
        "data": rows,
    }


@router.get("/retrieve")
def retrieve_metadata_context(
    question: str = Query(min_length=1, description="Natural language question"),
    table_limit: int = Query(default=5, ge=1, le=20),
    field_limit: int = Query(default=20, ge=1, le=100),
    fields_per_table: int = Query(default=12, ge=1, le=50),
) -> dict[str, object]:
    try:
        data = _retrieval_service().retrieve(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": data,
    }


@router.get("/context")
def build_metadata_context(
    question: str = Query(min_length=1, description="Natural language question"),
    table_limit: int = Query(default=3, ge=1, le=10),
    field_limit: int = Query(default=20, ge=1, le=100),
    fields_per_table: int = Query(default=10, ge=1, le=30),
) -> dict[str, object]:
    try:
        data = _context_service().build_context(
            question=question,
            table_limit=table_limit,
            field_limit=field_limit,
            fields_per_table=fields_per_table,
        )
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": data,
    }


@router.get("/fields")
def search_fields(
    q: str | None = Query(default=None, description="Keyword for field metadata"),
    table_id: str | None = Query(default=None, description="table_dictionary.bbs"),
    table_name: str | None = Query(default=None, description="table_dictionary.bywm"),
    limit: int = Query(default=100, ge=1, le=200),
) -> dict[str, object]:
    try:
        rows = _repository().search_fields(
            query=q,
            table_id=table_id,
            table_name=table_name,
            limit=limit,
        )
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "count": len(rows),
        "data": rows,
    }


@router.get("/tables/{table_id}/fields")
def list_table_fields(
    table_id: str,
    limit: int = Query(default=200, ge=1, le=200),
) -> dict[str, object]:
    try:
        rows = _repository().search_fields(table_id=table_id, limit=limit)
    except pymysql.MySQLError as exc:
        raise HTTPException(status_code=503, detail=f"metadata database unavailable: {exc.args[0]}") from exc

    return {
        "ok": True,
        "request_id": get_request_id(),
        "count": len(rows),
        "data": rows,
    }
