from app.repository.book_repo import BookRepository
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    
    async def get_books(self, db: Session, size: int, cursor: Optional[UUID], status=None, author=None):
        books, next_cursor = await self.repo.get_all(db, size, cursor, status, author)
        
        return {
            "items": books,
            "next_cursor": next_cursor
        }