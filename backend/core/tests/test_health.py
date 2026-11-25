import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_returns_ok(client: Client) -> None:
    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
