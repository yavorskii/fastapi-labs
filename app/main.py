from fastapi import FastAPI
from app.api.books import router as books_router
from app.api.auth import router as auth_router 

app = FastAPI(
    title="Library API - Lab 7",
    description="JWT Auth з Access & Refresh tokens",
    version="6.0.0"
)

app.include_router(auth_router) 
app.include_router(books_router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Library API (Lab 7)",
        "auth": "JWT with Refresh Flow enabled",
        "docs": "/docs"
    }