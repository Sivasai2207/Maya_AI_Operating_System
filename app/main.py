from fastapi import FastAPI
from sqlalchemy import text

from app.api.conversations import router as conversations_router
from app.core.config import settings
from app.database.session import engine


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(conversations_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Maya",
        "environment": settings.environment,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/db-health")
async def db_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }