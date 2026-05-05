from fastapi import APIRouter, HTTPException, status, Query, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.book import Book, BookCreate, BookStatus, BookListResponse 
from app.services.book_service import BookService
from app.database import get_db  
from app.api.deps import get_current_user 
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=BookListResponse)
async def get_books(
    status: Optional[BookStatus] = None, 
    author: Optional[str] = None, 
    limit: int = Query(10, ge=1, le=100),  
    offset: int = Query(0, ge=0),          
    db: AsyncIOMotorDatabase = Depends(get_db)          
):
    return await service.get_books(db, limit, offset, status, author)

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    book = await service.repo(db).get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate, 
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: str = Depends(get_current_user) 
):
    return await service.repo(db).add(db, book.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str, 
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: str = Depends(get_current_user) 
):
    success = await service.repo(db).delete(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None