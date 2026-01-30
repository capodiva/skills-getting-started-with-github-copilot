from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_contains_expected_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic smoke checks
    assert "Chess Club" in data
    assert "Basketball Team" in data


def test_signup_flow_and_duplicate_and_not_found():
    email = "testuser@example.com"

    # Sign up for Soccer Club (initially empty)
    resp = client.post("/activities/Soccer Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()["Soccer Club"]["participants"]

    # Duplicate signup should return 400
    resp_dup = client.post("/activities/Soccer Club/signup", params={"email": email})
    assert resp_dup.status_code == 400

    # Signing up for non-existent activity -> 404
    resp_nf = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b"})
    assert resp_nf.status_code == 404


def test_unregister_flow_and_errors():
    # Unregister existing initial participant from Basketball Team
    resp = client.delete("/activities/Basketball Team/participants", params={"email": "mason@mergington.edu"})
    assert resp.status_code == 200
    assert "mason@mergington.edu" not in client.get("/activities").json()["Basketball Team"]["participants"]

    # Unregistering a non-member should return 404
    resp_nf = client.delete("/activities/Basketball Team/participants", params={"email": "nosuch@example.com"})
    assert resp_nf.status_code == 404

    # Unregistering from a non-existent activity -> 404
    resp_nf2 = client.delete("/activities/NoActivity/participants", params={"email": "a@b"})
    assert resp_nf2.status_code == 404
