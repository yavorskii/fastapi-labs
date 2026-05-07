import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException, Request
from app.core.rate_limiter import rate_limit

@pytest.mark.asyncio
@patch("app.core.rate_limiter.r")
async def test_rate_limit_authenticated_success(mock_redis):
    mock_redis.zcard = AsyncMock(return_value=5)
    mock_request = AsyncMock(spec=Request)
    
    await rate_limit(mock_request, user_id="vladyslav")
    
    assert mock_redis.zadd.called

@pytest.mark.asyncio
@patch("app.core.rate_limiter.r")
async def test_rate_limit_authenticated_exceeded(mock_redis):
    mock_redis.zcard = AsyncMock(return_value=10)
    mock_request = AsyncMock(spec=Request)
    
    with pytest.raises(HTTPException) as exc:
        await rate_limit(mock_request, user_id="vladyslav")
    
    assert exc.value.status_code == 429

@pytest.mark.asyncio
@patch("app.core.rate_limiter.r")
async def test_rate_limit_anonymous_success(mock_redis):
    mock_redis.zcard = AsyncMock(return_value=1)
    mock_request = AsyncMock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    
    await rate_limit(mock_request, user_id=None)
    
    assert mock_redis.zadd.called

@pytest.mark.asyncio
@patch("app.core.rate_limiter.r")
async def test_rate_limit_anonymous_exceeded(mock_redis):
    mock_redis.zcard = AsyncMock(return_value=2)
    mock_request = AsyncMock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    
    with pytest.raises(HTTPException) as exc:
        await rate_limit(mock_request, user_id=None)
    
    assert exc.value.status_code == 429