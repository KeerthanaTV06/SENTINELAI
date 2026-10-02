"""FastAPI application entrypoint for SENTINEL-AI."""
from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from config import get_settings

# Configure application logging early to avoid other modules importing
# the stdlib logging before handlers are attached.
settings = get_settings()

# Import our app logger utility and configure based on settings
from app_logger import configure_logging
configure_logging(settings.LOG_LEVEL)

# Now import submodules that may obtain loggers
from backend.app.api.health import router as health_router
from backend.api.explainability import router as explain_router
from backend.app.api.models import router as models_router
from backend.app.api.datasets import router as datasets_router

logger = logging.getLogger("sentinel.app")

from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from typing import Callable
from cachetools import TTLCache

app = FastAPI(title="SENTINEL-AI", version="0.1.0")

# Security: configure CORS from settings if provided, fallback to restrictive default
allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
if settings.APP_ENV == "production":
    allowed_origins = ["https://your-production-domain.example"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Simple in-memory rate limiter middleware
RATE_LIMIT = 120  # requests
RATE_PERIOD = 60  # seconds
RATE_STORE: dict = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable):
        ip = request.client.host if request.client else "anonymous"
        now = time.time()
        window = RATE_STORE.get(ip, [])
        # remove expired
        window = [t for t in window if t > now - RATE_PERIOD]
        if len(window) >= RATE_LIMIT:
            return Response(status_code=429, content="Too Many Requests")
        window.append(now)
        RATE_STORE[ip] = window
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)

# Simple secure headers middleware
class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable):
        resp = await call_next(request)
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["Permissions-Policy"] = "geolocation=()"
        return resp

app.add_middleware(SecureHeadersMiddleware)

# Simple GET response cache
CACHE = TTLCache(maxsize=1024, ttl=30)

class SimpleCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable):
        if request.method == "GET":
            key = request.url.path + "?" + request.url.query
            if key in CACHE:
                data, headers, status = CACHE[key]
                return Response(content=data, status_code=status, headers=headers, media_type="application/json")
            response = await call_next(request)
            try:
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                CACHE[key] = (body, dict(response.headers), response.status_code)
                return Response(content=body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
            except Exception:
                return response
        else:
            return await call_next(request)

app.add_middleware(SimpleCacheMiddleware)

app.include_router(health_router, prefix="/api")
# Mount existing API routers under /api/v1 to maintain backward compatibility with tests
app.include_router(models_router, prefix="/api/v1")
app.include_router(datasets_router, prefix="/api/v1")
# Explainability router already defines /api/v1 paths internally, include without additional prefix
app.include_router(explain_router)


# Prometheus metrics endpoint (optional)
try:
    from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
    REQ_COUNT = Counter('sentinel_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])

    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        try:
            REQ_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=str(response.status_code)).inc()
        except Exception:
            pass
        return response

    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
except Exception:
    logger.info("prometheus_client not installed; /metrics endpoint disabled")


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting SENTINEL-AI application")
    # Future: initialize Kafka and Elasticsearch clients here


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Shutting down SENTINEL-AI application")


@app.exception_handler(Exception)
async def all_exception_handler(request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})