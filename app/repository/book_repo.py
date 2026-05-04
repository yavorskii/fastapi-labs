from sqlalchemy.orm import Session
from app.models.book_model import BookModel
from uuid import UUID
from typing import Optional

class BookRepository:
    async def get_all(self, db: Session, size: int, cursor: Optional[UUID], status=None, author=None):
        query = db.query(BookModel).order_by(BookModel.id)

        if status:
            query = query.filter(BookModel.status == status)
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        
        if cursor:
            query = query.filter(BookModel.id > cursor)
        
        books = query.limit(size).all()
        
        next_cursor = books[-1].id if len(books) == size else None
        
        return books, next_cursor

    async def add(self, db: Session, book_data: dict):
        db_book = BookModel(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    async def get_by_id(self, db: Session, book_id):
        return db.query(BookModel).filter(BookModel.id == book_id).first()

    async def delete(self, db: Session, book_id):
        book = self.get_by_id(db, book_id) 
        if book:
            db.delete(book)
            db.commit()
            return True
        return False