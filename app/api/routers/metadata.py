from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.config import get_settings
from app.core.request_context import get_request_id
from app.repositories.metadata_repository import MetadataRepository


router = APIRouter(prefix="/api/metadata", tags=["metadata"])


def _repository() -> MetadataRepository:
    return MetadataRepository(get_settings().metadata_db)


@router.get("/summary")
def metadata_summary() -> dict[str, object]:
    return {
        "ok": True,
        "request_id": get_request_id(),
        "data": _repository().get_summary(),
    }


@router.get("/tables")
def search_tables(
    q: str | None = Query(default=None, description="Keyword for table metadata"),
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, object]:
    rows = _repository().search_tables(query=q, limit=limit)
    return {
        "ok": True,
        "request_id": get_request_id(),
        "count": len(rows),
        "data": rows,
    }


@router.get("/fields")
def search_fields(
    q: str | None = Query(default=None, description="Keyword for field metadata"),
    table_id: str | None = Query(default=None, description="table_dictionary.bbs"),
    table_name: str | None = Query(default=None, description="table_dictionary.bywm"),
    limit: int = Query(default=100, ge=1, le=200),
) -> dict[str, object]:
    rows = _repository().search_fields(
        query=q,
        table_id=table_id,
        table_name=table_name,
        limit=limit,
    )
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
    rows = _repository().search_fields(table_id=table_id, limit=limit)
    return {
        "ok": True,
        "request_id": get_request_id(),
        "count": len(rows),
        "data": rows,
    }
