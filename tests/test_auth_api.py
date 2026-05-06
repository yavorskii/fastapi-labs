import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch



with patch("motor.motor_asyncio.AsyncIOMotorClient", return_value=MagicMock()):
    from app.main import app
    from app.database import get_db


async def override_get_db():
    mock_db = MagicMock()
    
    mock_db.users.find_one = AsyncMock(return_value=None)
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_auth_token_invalid_credentials():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        response = await ac.post("/auth/token", data={
            "username": "nonexistent",
            "password": "wrongpassword"
        })
    
    assert response.status_code == 401


@pytest.fixture(autouse=True)
def cleanup():
    yield
    app.dependency_overrides = {}