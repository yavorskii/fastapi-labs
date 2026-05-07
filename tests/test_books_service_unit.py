import pytest
from unittest.mock import AsyncMock

from app.services.book_service import BookService


@pytest.mark.anyio
async def test_service_get_books_delegates_to_repo(monkeypatch):
    service = BookService()
    repo_mock = type("Repo", (), {"get_all": AsyncMock(return_value=["ok"])})()
    monkeypatch.setattr(service, "repo", repo_mock)

    db = object()
    res = await service.get_books(db, limit=10, offset=5, status="наявна", author="martin")

    assert res == ["ok"]
    repo_mock.get_all.assert_awaited_once_with(db, 10, 5, "наявна", "martin")
