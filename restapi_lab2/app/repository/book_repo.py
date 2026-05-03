from sqlalchemy.orm import Session
from app.models.book_model import BookModel

class BookRepository:
    async def get_all(self, db: Session, limit: int, offset: int, status=None, author=None):
        query = db.query(BookModel)
        
        
        if status:
            query = query.filter(BookModel.status == status)
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        
        return query.offset(offset).limit(limit).all()

    async def add(self, db: Session, book_data: dict):
        db_book = BookModel(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    async def get_by_id(self, db: Session, book_id):
        return db.query(BookModel).filter(BookModel.id == book_id).first()

    async def delete(self, db: Session, book_id):
        book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False