import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_unregister_participant_from_activity(client):
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    # ensure the participant is not already present
    activity = activities[activity_name]
    if email in activity["participants"]:
        activity["participants"].remove(email)

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
