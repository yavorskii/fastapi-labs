from fastapi import FastAPI
from app.database import engine, Base
from app.api.books import router

from app.models.book_model import BookModel 


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library API - Lab 3",
    description="API з використанням Cursor Pagination для оптимізації запитів",
    version="3.0.0"
)

app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Library API (Lab 3)",
        "features": "Cursor Pagination is enabled",
        "docs": "/docs"
    }