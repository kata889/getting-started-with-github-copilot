def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    email = "new.student@mergington.edu"
    endpoint = "/activities/Chess Club/signup"

    first_response = client.post(endpoint, params={"email": email})
    second_response = client.post(endpoint, params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Student is already signed up for this activity"
    )
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert participants.count(email) == 1


def test_unregister_removes_participant(client):
    email = "new.student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_unregistered_participant(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Student is not signed up for this activity"
    )
