from app.repository.mongo_repo import MongoBookRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

class BookService:
    def __init__(self):
        self.repo = MongoBookRepository

    async def get_books(self, db: AsyncIOMotorDatabase, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None):
        repo_instance = self.repo(db)
        
        books = await repo_instance.get_all(db, limit, offset, status, author)
        
        total = await db.books.count_documents(self._build_query(status, author))
        
        return {
            "items": books,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def _build_query(self, status: Optional[str] = None, author: Optional[str] = None):
        query = {}
        if status:
            query["status"] = status
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        return query