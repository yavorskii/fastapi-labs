import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repository.mongo_repo import MongoBookRepository
from bson import ObjectId

@pytest.mark.asyncio
async def test_get_by_id_invalid_oid():
    mock_db = MagicMock()
    repo = MongoBookRepository(mock_db)
    result = await repo.get_by_id(mock_db, "invalid_id")
    assert result is None

@pytest.mark.asyncio
async def test_add_book_repo():
    mock_db = MagicMock()
    mock_db.books.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))
    repo = MongoBookRepository(mock_db)
    
    book_data = {"title": "New Book", "author": "Vlad"}
    result = await repo.add(mock_db, book_data)
    
    assert "id" in result
    assert result["title"] == "New Book"