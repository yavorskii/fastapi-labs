import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.repository.book_repo import BookRepository


@pytest.mark.anyio
async def test_repo_get_all_applies_filters_and_cursor(monkeypatch):
    repo = BookRepository()

    query = MagicMock(name="query")
    query.order_by.return_value = query
    query.filter.return_value = query
    query.limit.return_value = query

    book1 = MagicMock()
    book2 = MagicMock()
    book1.id = uuid4()
    book2.id = uuid4()
    query.all.return_value = [book1, book2]

    db = MagicMock(name="db")
    db.query.return_value = query

    cursor = uuid4()
    books, next_cursor = await repo.get_all(db, size=2, cursor=cursor, status="наявна", author="martin")

    assert books == [book1, book2]
    assert next_cursor == book2.id
    query.order_by.assert_called_once()
    assert query.filter.call_count == 3
    query.limit.assert_called_once_with(2)
