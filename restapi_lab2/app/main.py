from fastapi import FastAPI
from app.database import engine, Base
from app.api.books import router
from app.models.book_model import BookModel 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API - Lab 2")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Library API. Go to /docs for Swagger"}