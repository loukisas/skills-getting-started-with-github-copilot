import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    initial = deepcopy(activities)
    monkeypatch.setattr("src.app.activities", initial)
    yield


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity(client):
    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
    assert response.status_code == 200
    assert "Signed up student@mergington.edu" in response.json()["message"]


def test_signup_duplicate_returns_400(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity_returns_404(client):
    response = client.post("/activities/NotFound/signup?email=user@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant(client):
    response = client.delete("/activities/Chess Club/participants?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "Removed michael@mergington.edu" in response.json()["message"]


def test_remove_participant_invalid_activity(client):
    response = client.delete("/activities/DoesNotExist/participants?email=user@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_not_found(client):
    response = client.delete("/activities/Chess Club/participants?email=nonexistent@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
