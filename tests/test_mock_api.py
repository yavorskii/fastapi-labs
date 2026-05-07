import pytest
import httpx

@pytest.mark.asyncio
async def test_mock_books_list():
    async with httpx.AsyncClient(base_url="http://localhost:4010") as client:
        response = await client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_mock_auth_token():
    async with httpx.AsyncClient(base_url="http://localhost:4010") as client:
        payload = {"username": "testuser", "password": "password123"}
        response = await client.post("/auth/token", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()