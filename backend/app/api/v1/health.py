
from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from qdrant_client.http.exceptions import UnexpectedResponse
from redis.exceptions import RedisError

from app.core.config import settings
from app.db.mongodb import MongoDB
from app.db.qdrant import QdrantDB
from app.db.redis import RedisDB

router = APIRouter()


@router.get("/health/live", tags=["Health"])
async def liveness_check():
    return {
        "status": "alive",
        "application": settings.app_name,
    }


@router.get("/health/ready", tags=["Health"])
async def readiness_check():
    checks = {
        "mongodb": "connected",
        "redis": "connected",
        "qdrant": "connected",
    }

    try:
        await MongoDB.get_database().command("ping")
    except (PyMongoError, RuntimeError):
        checks["mongodb"] = "disconnected"

    try:
        await RedisDB.get_client().ping()
    except (RedisError, RuntimeError):
        checks["redis"] = "disconnected"

    try:
        await QdrantDB.get_client().get_collections()
    except (UnexpectedResponse, RuntimeError, TimeoutError, ConnectionError):
        checks["qdrant"] = "disconnected"

    if "disconnected" in checks.values():
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "application": settings.app_name,
                "checks": checks,
            },
        )

    return {
        "status": "ready",
        "application": settings.app_name,
        "checks": checks,
    }


@router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "environment": settings.environment,
        "message": "RepoMind backend is running",
    }
