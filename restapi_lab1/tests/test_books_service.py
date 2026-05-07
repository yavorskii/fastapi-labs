import pytest
from unittest.mock import AsyncMock

from app.services.book_service import BookService


@pytest.mark.anyio
async def test_get_books_returns_all_when_no_filters(monkeypatch):
    service = BookService()
    monkeypatch.setattr(
        service,
        "repo",
        type("Repo", (), {"get_all": AsyncMock(return_value=[{"title": "A", "author": "X", "year": 2020, "status": "наявна"}])})(),
    )

    books = await service.get_books()

    assert books == [{"title": "A", "author": "X", "year": 2020, "status": "наявна"}]


@pytest.mark.anyio
async def test_get_books_filters_by_status(monkeypatch):
    service = BookService()
    monkeypatch.setattr(
        service,
        "repo",
        type(
            "Repo",
            (),
            {
                "get_all": AsyncMock(
                    return_value=[
                        {"title": "A", "author": "X", "year": 2020, "status": "наявна"},
                        {"title": "B", "author": "Y", "year": 2019, "status": "видана"},
                    ]
                )
            },
        )(),
    )

    books = await service.get_books(status="наявна")

    assert books == [{"title": "A", "author": "X", "year": 2020, "status": "наявна"}]


@pytest.mark.anyio
async def test_get_books_filters_by_author_substring_case_insensitive(monkeypatch):
    service = BookService()
    monkeypatch.setattr(
        service,
        "repo",
        type(
            "Repo",
            (),
            {
                "get_all": AsyncMock(
                    return_value=[
                        {"title": "A", "author": "Robert Martin", "year": 2008, "status": "наявна"},
                        {"title": "B", "author": "Martin Fowler", "year": 1999, "status": "наявна"},
                        {"title": "C", "author": "Kent Beck", "year": 2002, "status": "видана"},
                    ]
                )
            },
        )(),
    )

    books = await service.get_books(author="mArTiN")

    assert [b["title"] for b in books] == ["A", "B"]


@pytest.mark.anyio
async def test_get_books_sorts_by_title(monkeypatch):
    service = BookService()
    monkeypatch.setattr(
        service,
        "repo",
        type(
            "Repo",
            (),
            {
                "get_all": AsyncMock(
                    return_value=[
                        {"title": "C", "author": "X", "year": 2020, "status": "наявна"},
                        {"title": "A", "author": "X", "year": 2018, "status": "наявна"},
                        {"title": "B", "author": "X", "year": 2019, "status": "наявна"},
                    ]
                )
            },
        )(),
    )

    books = await service.get_books(sort_by="title")

    assert [b["title"] for b in books] == ["A", "B", "C"]


@pytest.mark.anyio
async def test_get_books_sorts_by_year(monkeypatch):
    service = BookService()
    monkeypatch.setattr(
        service,
        "repo",
        type(
            "Repo",
            (),
            {
                "get_all": AsyncMock(
                    return_value=[
                        {"title": "A", "author": "X", "year": 2020, "status": "наявна"},
                        {"title": "B", "author": "X", "year": 2018, "status": "наявна"},
                        {"title": "C", "author": "X", "year": 2019, "status": "наявна"},
                    ]
                )
            },
        )(),
    )

    books = await service.get_books(sort_by="year")

    assert [b["year"] for b in books] == [2018, 2019, 2020]
