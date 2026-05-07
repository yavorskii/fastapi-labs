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
