from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.book import Book, BookCreate, BookStatus
from app.services.book_service import BookService
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[Book])
async def get_books(
    status: Optional[BookStatus] = None, 
    author: Optional[str] = None, 
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$")
):
    return await service.get_books(status, author, sort_by)

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID):
    book = await service.repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await service.repo.add(book.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await service.repo.delete(book_id)
    return None