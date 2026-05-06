import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.book_service import BookService

@pytest.mark.asyncio
async def test_get_books_service_logic():
    service = BookService()
    mock_db = AsyncMock()
    
    
    mock_repo_instance = AsyncMock()
    mock_repo_instance.get_all.return_value = [{"id": "1", "title": "Test Book"}]
    service.repo = MagicMock(return_value=mock_repo_instance)
    
    
    mock_db.books.count_documents = AsyncMock(return_value=1)
    
    result = await service.get_books(mock_db, limit=10, offset=0)
    
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["title"] == "Test Book"