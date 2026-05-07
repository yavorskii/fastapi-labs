import pytest
import httpx

from app.main import app

@pytest.mark.anyio
async def test_create_and_get_book():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books/", json={
            "title": "Clean Code",
            "author": "Robert Martin",
            "year": 2008,
            "status": "наявна"
        })
        assert response.status_code == 201
        book_id = response.json()["id"]

        get_res = await ac.get(f"/books/{book_id}")
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Clean Code"

@pytest.mark.anyio
async def test_pagination_limit():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        for i in range(2):
            await ac.post("/books/", json={
                "title": f"Pagination Book {i}",
                "author": "Tester",
                "year": 2024,
                "status": "наявна"
            })

        response = await ac.get("/books/", params={"limit": 1, "offset": 0})
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 1


@pytest.mark.anyio
async def test_get_books_filters_by_status_and_author():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/books/", json={"title": "A", "author": "Kent Beck", "year": 2002, "status": "наявна"})
        await ac.post("/books/", json={"title": "B", "author": "Robert Martin", "year": 2008, "status": "видана"})
        await ac.post("/books/", json={"title": "C", "author": "Martin Fowler", "year": 1999, "status": "наявна"})

        res = await ac.get("/books/", params={"status": "наявна", "author": "martin"})
        assert res.status_code == 200
        titles = [b["title"] for b in res.json()]
        assert titles == ["C"]


@pytest.mark.anyio
async def test_delete_book_returns_404_when_missing():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.delete("/books/00000000-0000-0000-0000-000000000000")
        assert res.status_code == 404
        assert res.json()["detail"] == "Book not found"
