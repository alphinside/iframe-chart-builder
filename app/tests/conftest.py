import pytest
from fastapi.testclient import TestClient

from app.main import get_app  # noqa: E402


@pytest.fixture()
def test_client() -> TestClient:
    app = get_app()
    client = TestClient(app)

    yield client
