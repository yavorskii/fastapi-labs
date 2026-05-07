import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pytest
from bson import ObjectId

from app.main import app
from app.database import get_db


class _DeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count


class _InsertOneResult:
    def __init__(self, inserted_id: ObjectId):
        self.inserted_id = inserted_id


class FakeCursor:
    def __init__(self, docs: List[Dict[str, Any]]):
        self._docs = docs
        self._skip = 0
        self._limit: Optional[int] = None

    def skip(self, n: int):
        self._skip = n
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    async def to_list(self, length: int):
        docs = self._docs[self._skip :]
        if self._limit is not None:
            docs = docs[: self._limit]
        return [dict(d) for d in docs]


class FakeBooksCollection:
    def __init__(self):
        self._docs: List[Dict[str, Any]] = []

    def _match(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for key, value in query.items():
            if key == "author" and isinstance(value, dict) and "$regex" in value:
                pattern = value["$regex"]
                options = value.get("$options", "")
                flags = re.IGNORECASE if "i" in options else 0
                if not re.search(pattern, doc.get("author", ""), flags=flags):
                    return False
            else:
                if doc.get(key) != value:
                    return False
        return True

    def find(self, query: Dict[str, Any]):
        matched = [d for d in self._docs if self._match(d, query)]
        return FakeCursor(matched)

    async def count_documents(self, query: Dict[str, Any]):
        return sum(1 for d in self._docs if self._match(d, query))

    async def insert_one(self, book_data: Dict[str, Any]):
        _id = ObjectId()
        doc = dict(book_data)
        doc["_id"] = _id
        self._docs.append(doc)
        return _InsertOneResult(_id)

    async def find_one(self, query: Dict[str, Any]):
        _id = query.get("_id")
        for d in self._docs:
            if d.get("_id") == _id:
                return dict(d)
        return None

    async def delete_one(self, query: Dict[str, Any]):
        _id = query.get("_id")
        before = len(self._docs)
        self._docs = [d for d in self._docs if d.get("_id") != _id]
        return _DeleteResult(before - len(self._docs))


@dataclass
class FakeMongoDB:
    books: FakeBooksCollection


@pytest.fixture()
def fake_db():
    return FakeMongoDB(books=FakeBooksCollection())


@pytest.fixture(autouse=True)
def _override_db(fake_db):
    async def _override():
        yield fake_db

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.pop(get_db, None)
