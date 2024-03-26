import httpx
from httpx import AsyncClient
import os
import pytest


async def test_post_route_with_auth(ac):
    response = await ac.post('/api/posts', json={
        "year": 2024,
        "tags": "#Круто",
        "title": "Крутой год",
        "desc": "<p> Круто </p>"
    }, headers={
        "Authorization": os.getenv("BEARER")
    })

    assert response.status_code == 200

@pytest.mark.parametrize('routes', ['/api/posts', '/api/posts/2024'])
async def test_get_routes(ac, routes):
    response = await ac.get(routes)
    assert response.status_code == 200
    assert len(response.json()) == 1

async def test_post_route_without_auth(ac):
    response = await ac.post('/api/posts', json={
        "year": 2024,
        "tags": "#Круто",
        "title": "Крутой год",
        "desc": "<p> Круто </p>"
    })

    assert response.status_code == 401

async def test_put_route(ac):
    response = await ac.put('/api/posts/2024', json={
        "year": 2024,
        "tags": "#Круто",
        "title": "Крутой",
        "desc": "<p> Круто </p>"
    },headers={
        "Authorization": os.getenv("BEARER")
    })

    assert response.status_code == 200
    assert "Крутой" in response.json()['title']

async def test_delete_route(ac):
    response = await ac.delete('/api/posts/2024',  headers={
        "Authorization": os.getenv("BEARER")
    })

    assert response.status_code == 200

