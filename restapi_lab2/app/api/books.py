from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from app.schemas.book import Book, BookCreate, BookStatus
from app.services.book_service import BookService
from app.database import get_db  
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[Book])
async def get_books(
    status: Optional[BookStatus] = None, 
    author: Optional[str] = None, 
    limit: int = Query(10, ge=1, le=100),  
    offset: int = Query(0, ge=0),          
    db: Session = Depends(get_db)          
):
    
    return await service.get_books(db, limit, offset, status, author)

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID, db: Session = Depends(get_db)):
    book = await service.repo.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):

    return await service.repo.add(db, book.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    success = await service.repo.delete(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None