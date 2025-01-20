from main import app
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from modules.users.models import User


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = User(username="testuser", password="goodpassword")
    return db


@pytest.fixture
def mock_token_functions():
    mock_create_access_token = MagicMock(return_value="mocked_token")
    mock_verify_token = MagicMock()
    return mock_create_access_token, mock_verify_token

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_verify_token_url(client, mock_token_functions):
    _, mock_verify_token = mock_token_functions

    token = "mocked_token"

    response = client.get(f"/api/verify-token/{token}")

    assert response.status_code == 403
    assert response.json() == {'detail': 'Token is invalide or expired'}


def test_incorrect_login(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    form_data = {"username": "wronguser", "password": "wrongpassword"}

    response = client.post("/api/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


