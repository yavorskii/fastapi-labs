import pytest
import httpx

from app.main import app


@pytest.mark.anyio
async def test_create_get_list_and_delete_book():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        create_res = await ac.post(
            "/books/",
            json={"title": "Clean Code", "author": "Robert Martin", "year": 2008, "status": "наявна", "description": None},
        )
        assert create_res.status_code == 201
        book_id = create_res.json()["id"]

        get_res = await ac.get(f"/books/{book_id}")
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Clean Code"

        list_res = await ac.get("/books/", params={"limit": 10, "offset": 0})
        assert list_res.status_code == 200
        data = list_res.json()
        assert data["total"] == 1
        assert data["limit"] == 10
        assert data["offset"] == 0
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == book_id

        del_res = await ac.delete(f"/books/{book_id}")
        assert del_res.status_code == 204

        missing_res = await ac.get(f"/books/{book_id}")
        assert missing_res.status_code == 404


@pytest.mark.anyio
async def test_list_books_filters_and_paginates():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/books/", json={"title": "A", "author": "Kent Beck", "year": 2002, "status": "наявна"})
        await ac.post("/books/", json={"title": "B", "author": "Martin Fowler", "year": 1999, "status": "наявна"})
        await ac.post("/books/", json={"title": "C", "author": "Robert Martin", "year": 2008, "status": "видана"})

        page1 = await ac.get("/books/", params={"limit": 1, "offset": 0, "status": "наявна", "author": "martin"})
        assert page1.status_code == 200
        data1 = page1.json()
        assert data1["total"] == 1
        assert len(data1["items"]) == 1
        assert data1["items"][0]["title"] == "B"


@pytest.mark.anyio
async def test_delete_returns_404_for_invalid_id():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.delete("/books/not-an-objectid")
        assert res.status_code == 404
        assert res.json()["detail"] == "Book not found"
