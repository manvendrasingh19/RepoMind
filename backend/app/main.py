
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.db.indexes import initialize_indexes
from app.db.mongodb import MongoDB
from app.db.qdrant import QdrantDB
from app.db.redis import RedisDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{settings.app_name} backend starting...")

    try:
        # Establish infrastructure connections.
        await MongoDB.connect()
        await RedisDB.connect()
        await QdrantDB.connect()

        await initialize_indexes(MongoDB.get_database())
        print("MongoDB collections and indexes initialized.")

        app.state.mongodb = MongoDB.database
        app.state.redis = RedisDB.get_client()
        app.state.qdrant = QdrantDB.get_client()

        print("All infrastructure services connected.")

        yield

    finally:
        # Close connections in reverse order.
        await QdrantDB.close()
        await RedisDB.close()
        await MongoDB.close()

        print(f"{settings.app_name} backend shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered codebase intelligence platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "message": "Welcome to the RepoMind API",
        "docs": "/docs",
    }
