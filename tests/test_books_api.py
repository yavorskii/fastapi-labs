import pytest
import httpx
from unittest.mock import AsyncMock
from uuid import uuid4

from app.main import app
import app.api.books as books_api


@pytest.mark.anyio
async def test_get_books_uses_service(monkeypatch):
    book_id = uuid4()
    expected = [
        {"id": book_id, "title": "A", "author": "Robert Martin", "year": 2008, "status": "наявна", "description": None}
    ]
    get_books_mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(books_api, "service", books_api.service)
    monkeypatch.setattr(books_api.service, "get_books", get_books_mock)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/books/", params={"status": "наявна", "author": "martin", "sort_by": "year"})

    assert res.status_code == 200
    assert res.json()[0]["id"] == str(book_id)
    get_books_mock.assert_awaited_once()
    called_status, called_author, called_sort_by = get_books_mock.await_args.args
    assert called_status == "наявна"
    assert called_author == "martin"
    assert called_sort_by == "year"


@pytest.mark.anyio
async def test_get_book_returns_404_when_missing(monkeypatch):
    get_by_id_mock = AsyncMock(return_value=None)
    monkeypatch.setattr(books_api.service.repo, "get_by_id", get_by_id_mock)

    missing_id = uuid4()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get(f"/books/{missing_id}")

    assert res.status_code == 404
    assert res.json()["detail"] == "Book not found"
    get_by_id_mock.assert_awaited_once_with(missing_id)


@pytest.mark.anyio
async def test_create_book_calls_repo_add(monkeypatch):
    created_id = uuid4()
    add_mock = AsyncMock(
        return_value={
            "id": created_id,
            "title": "Clean Code",
            "author": "Robert Martin",
            "year": 2008,
            "status": "наявна",
            "description": None,
        }
    )
    monkeypatch.setattr(books_api.service.repo, "add", add_mock)

    payload = {"title": "Clean Code", "author": "Robert Martin", "year": 2008, "status": "наявна", "description": None}
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/books/", json=payload)

    assert res.status_code == 201
    assert res.json()["id"] == str(created_id)
    add_mock.assert_awaited_once()
    assert add_mock.await_args.args[0]["title"] == "Clean Code"


@pytest.mark.anyio
async def test_delete_book_calls_repo_delete(monkeypatch):
    delete_mock = AsyncMock(return_value=True)
    monkeypatch.setattr(books_api.service.repo, "delete", delete_mock)

    book_id = uuid4()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.delete(f"/books/{book_id}")

    assert res.status_code == 204
    delete_mock.assert_awaited_once_with(book_id)
