"""Health and readiness endpoints."""
from __future__ import annotations

from fastapi import APIRouter
from starlette.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger("sentinel.health")


@router.get("/health", response_class=JSONResponse)
async def health() -> JSONResponse:
    """Return health status for the service.

    This is a lightweight endpoint intended for liveness checks.
    """
    payload = {"status": "ok"}
    logger.debug("Health check responded with %s", payload)
    return JSONResponse(status_code=200, content=payload)


@router.get("/ready", response_class=JSONResponse)
async def ready() -> JSONResponse:
    """Return readiness status for the service.

    In future this will check connectivity to critical dependencies such as
    Kafka and Elasticsearch.
    """
    payload = {"status": "ready"}
    logger.debug("Readiness check responded with %s", payload)
    return JSONResponse(status_code=200, content=payload)
