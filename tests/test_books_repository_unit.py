import pytest
from unittest.mock import MagicMock

from app.repository.book_repo import BookRepository


@pytest.mark.anyio
async def test_repo_get_all_applies_pagination_and_filters(monkeypatch):
    repo = BookRepository()

    query = MagicMock(name="query")
    query.filter.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query
    query.all.return_value = ["result"]

    db = MagicMock(name="db")
    db.query.return_value = query

    res = await repo.get_all(db, limit=2, offset=3, status="наявна", author="martin")

    assert res == ["result"]
    assert db.query.call_count == 1
    assert query.filter.call_count == 2
    query.offset.assert_called_once_with(3)
    query.limit.assert_called_once_with(2)
    query.all.assert_called_once_with()
