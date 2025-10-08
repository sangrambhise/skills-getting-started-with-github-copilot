from fastapi.testclient import TestClient
from src import app as application_module

client = TestClient(application_module.app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Should be a dict mapping activity names to details
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_delete_participant():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure email not already present
    res = client.get("/activities")
    assert res.status_code == 200
    participants = res.json()[activity]["participants"]
    if email in participants:
        # Remove first so test can proceed deterministically
        r = client.delete(f"/activities/{activity}/participants?email={email}")
        assert r.status_code in (200, 404)

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json()["message"]

    # Verify present
    r2 = client.get("/activities")
    assert r2.status_code == 200
    assert email in r2.json()[activity]["participants"]

    # Delete
    r3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r3.status_code == 200
    assert "Unregistered" in r3.json()["message"]

    # Verify removed
    r4 = client.get("/activities")
    assert email not in r4.json()[activity]["participants"]
