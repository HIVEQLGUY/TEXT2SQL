from __future__ import annotations

from fastapi import APIRouter

from app.clients.mysql import ping_database
from app.core.config import get_settings
from app.core.request_context import get_request_id


router = APIRouter(tags=["health"])


@router.get("/api/health")
def health_check() -> dict[str, object]:
    settings = get_settings()
    return {
        "ok": True,
        "app": settings.app_name,
        "environment": settings.environment,
        "request_id": get_request_id(),
        "metadata_db": settings.metadata_db.safe_info(),
        "warehouse_db": settings.warehouse_db.safe_info(),
    }


@router.get("/api/ready")
def readiness_check() -> dict[str, object]:
    settings = get_settings()
    missing = settings.missing_required_values()
    return {
        "ok": not missing,
        "missing": missing,
        "request_id": get_request_id(),
    }


@router.get("/api/health/db")
def database_health_check() -> dict[str, object]:
    settings = get_settings()
    return {
        "ok": True,
        "request_id": get_request_id(),
        "metadata_db": ping_database(settings.metadata_db),
        "warehouse_db": ping_database(settings.warehouse_db),
    }
