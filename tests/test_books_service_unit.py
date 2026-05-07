import pytest
from unittest.mock import AsyncMock

from app.services.book_service import BookService


@pytest.mark.anyio
async def test_service_wraps_repo_response(monkeypatch):
    service = BookService()
    repo_mock = type("Repo", (), {"get_all": AsyncMock(return_value=(["b"], "cursor"))})()
    monkeypatch.setattr(service, "repo", repo_mock)

    db = object()
    res = await service.get_books(db, size=10, cursor=None, status="наявна", author="martin")

    assert res == {"items": ["b"], "next_cursor": "cursor"}
    repo_mock.get_all.assert_awaited_once_with(db, 10, None, "наявна", "martin")
