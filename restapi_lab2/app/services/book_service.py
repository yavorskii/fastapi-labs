from app.repository.book_repo import BookRepository
from sqlalchemy.orm import Session

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, db: Session, limit: int, offset: int, status=None, author=None):
        return await self.repo.get_all(db, limit, offset, status, author)