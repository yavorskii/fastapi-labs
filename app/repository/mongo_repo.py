from bson import ObjectId
from typing import List, Optional

class MongoBookRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db.books
        self.users_collection = db.users 

    async def get_all(self, db, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None):
        query = {}
        if status:
            query["status"] = status
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        
        cursor = self.collection.find(query).skip(offset).limit(limit)
        books = await cursor.to_list(length=limit)
        
        for book in books:
            book["id"] = str(book.pop("_id"))
        return books

    async def add(self, db, book_data: dict):
        result = await self.collection.insert_one(book_data)
        book_data["id"] = str(result.inserted_id)
        return book_data

    async def get_by_id(self, db, book_id: str):
        if not ObjectId.is_valid(book_id):
            return None
        book = await self.collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book["id"] = str(book.pop("_id"))
        return book

    async def delete(self, db, book_id: str):
        if not ObjectId.is_valid(book_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

    async def get_user(self, username: str):
        return await self.users_collection.find_one({"username": username})

    async def create_user(self, user_data: dict):
        await self.users_collection.insert_one(user_data)
        return user_data