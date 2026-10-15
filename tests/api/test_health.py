async def test_health_returns_ok(client):
    response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "app_name" in body
    assert "version" in body


async def test_health_does_not_expose_internal_config(client):
    response = await client.get("/health")

    assert set(response.json().keys()) == {"status", "app_name", "version"}


async def test_unknown_route_returns_404(client):
    response = await client.get("/does-not-exist")

    assert response.status_code == 404