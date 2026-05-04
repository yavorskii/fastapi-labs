from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from app.schemas.book import Book, BookCreate, BookStatus, BookListResponse 
from app.services.book_service import BookService
from app.database import get_db  
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()


@router.get("/", response_model=BookListResponse)
async def get_books(
    status: Optional[BookStatus] = None, 
    author: Optional[str] = None, 
    size: int = Query(10, ge=1, le=100),  
    cursor: Optional[UUID] = Query(None), 
    db: Session = Depends(get_db)          
):
    return await service.get_books(db, size, cursor, status, author)

