from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity():
    email = "test.signup@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_duplicate():
    email = "duplicate.student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 409
    assert response.json()["detail"] == "Already registered"


def test_remove_participant():
    email = "remove.student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}
