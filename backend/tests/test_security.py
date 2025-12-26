import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_access_protected_route_without_token():
    # Use transport for newer httpx versions
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Removed /api/v1 to match main.py
        response = await ac.get("/transactions")
    assert response.status_code == 401

@pytest.mark.anyio
async def test_invalid_token_format():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer not-a-real-token"}
        response = await ac.get("/transactions", headers=headers)
    assert response.status_code == 401