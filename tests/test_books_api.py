import pytest
import httpx

from app.main import app
from app.database import SessionLocal
from app.models.book_model import BookModel


def _seed_books():
    db = SessionLocal()
    try:
        b1 = BookModel(title="A", author="Robert Martin", year=2008, status="наявна", description=None)
        b2 = BookModel(title="B", author="Martin Fowler", year=1999, status="наявна", description=None)
        b3 = BookModel(title="C", author="Kent Beck", year=2002, status="видана", description=None)
        db.add_all([b1, b2, b3])
        db.commit()
        db.refresh(b1)
        db.refresh(b2)
        db.refresh(b3)
        return b1, b2, b3
    finally:
        db.close()


@pytest.mark.anyio
async def test_get_books_returns_items_and_next_cursor():
    b1, b2, b3 = _seed_books()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res1 = await ac.get("/books/", params={"size": 2})
        assert res1.status_code == 200
        data1 = res1.json()
        assert len(data1["items"]) == 2
        assert data1["next_cursor"] == data1["items"][-1]["id"]
        first_page_ids = {item["id"] for item in data1["items"]}
        assert first_page_ids.issubset({str(b1.id), str(b2.id), str(b3.id)})

        res2 = await ac.get("/books/", params={"size": 2, "cursor": data1["next_cursor"]})
        assert res2.status_code == 200
        data2 = res2.json()
        assert len(data2["items"]) == 1
        assert data2["items"][0]["id"] not in first_page_ids
        assert data2["next_cursor"] is None


@pytest.mark.anyio
async def test_get_books_filters_by_status_and_author():
    _seed_books()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/books/", params={"size": 10, "status": "наявна", "author": "fowler"})
        assert res.status_code == 200
        data = res.json()
        assert [b["title"] for b in data["items"]] == ["B"]
        assert data["next_cursor"] is None


@pytest.mark.anyio
async def test_create_book_then_list_contains_it():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "title": "New Book",
            "author": "Test Author",
            "description": "Desc",
            "year": 2024,
            "status": "наявна",
        }
        created = await ac.post("/books/", json=payload)
        assert created.status_code == 201
        created_data = created.json()
        assert created_data["title"] == payload["title"]
        assert created_data["author"] == payload["author"]
        assert "id" in created_data

        listed = await ac.get("/books/", params={"size": 10, "author": "Test Author"})
        assert listed.status_code == 200
        listed_items = listed.json()["items"]
        assert any(item["id"] == created_data["id"] for item in listed_items)
