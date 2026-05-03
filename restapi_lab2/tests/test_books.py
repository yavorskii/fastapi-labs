import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_book():
    async with AsyncClient(app=app, base_url="http://test") as ac:
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

@pytest.mark.asyncio
async def test_pagination_limit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
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