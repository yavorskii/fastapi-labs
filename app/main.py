import asyncio

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app.api.books import router

from app.models.book_model import BookModel  # noqa: F401

app = FastAPI(
    title="Library API - Lab 3",
    description="API з використанням Cursor Pagination для оптимізації запитів",
    version="3.0.0"
)

app.include_router(router)

@app.on_event("startup")
async def _startup_create_tables() -> None:
    max_attempts = 30
    delay_seconds = 1.0

    for attempt in range(1, max_attempts + 1):
        try:
            await asyncio.to_thread(Base.metadata.create_all, bind=engine)
            return
        except OperationalError:
            if attempt == max_attempts:
                raise
            await asyncio.sleep(delay_seconds)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Library API (Lab 3)",
        "features": "Cursor Pagination is enabled",
        "docs": "/docs"
    }
