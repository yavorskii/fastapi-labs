from sqlalchemy.orm import Session
from app.models.book_model import BookModel

class BookRepository:
    async def get_all(self, db: Session, limit: int, offset: int):
        return db.query(BookModel).offset(offset).limit(limit).all()

    async def add(self, db: Session, book_data: dict):
        db_book = BookModel(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book