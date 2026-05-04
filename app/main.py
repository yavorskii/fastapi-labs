from fastapi import FastAPI
from app.api.books import router

app = FastAPI(
    title="Library API - Lab 4",
    description="API з використанням MongoDB та Limit-Offset пагінації",
    version="4.0.0"
)

app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Library API (Lab 4)",
        "database": "MongoDB",
        "pagination": "Limit-Offset",
        "docs": "/docs"
    }