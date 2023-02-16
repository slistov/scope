from fastapi.testclient import TestClient
import pytest
from src.scope.entrypoints.fastapi_app import app


client = TestClient(app)


@pytest.fixture
def test_client():
    return client
