def test_get_activities_returns_all_activities_with_participants(client):
    # Arrange
    expected_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert expected_names.issubset(body.keys())
    assert "michael@mergington.edu" in body["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Art Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()["Art Club"]["participants"]


def test_signup_rejects_duplicate_email(client):
    # Arrange
    email = "michael@mergington.edu"
    before = client.get("/activities").json()["Chess Club"]["participants"][:]

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert client.get("/activities").json()["Chess Club"]["participants"] == before


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_returns_404_when_not_signed_up(client):
    # Arrange
    email = "stranger@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
