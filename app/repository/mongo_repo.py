from bson import ObjectId
from typing import List, Optional

class MongoBookRepository:
    def __init__(self, db):
        self.collection = db.books

    def get_all(self, db, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None):
        query = {}
        if status:
            query["status"] = status
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        
        cursor = self.collection.find(query).skip(offset).limit(limit)
        books = list(cursor)
        
        for book in books:
            book["id"] = str(book.pop("_id"))
        return books

    def add(self, db, book_data: dict):
        result = self.collection.insert_one(book_data)
        book_data["id"] = str(result.inserted_id)
        return book_data

    def get_by_id(self, db, book_id: str):
        if not ObjectId.is_valid(book_id):
            return None
        book = self.collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book["id"] = str(book.pop("_id"))
        return book

    def delete(self, db, book_id: str):
        if not ObjectId.is_valid(book_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0