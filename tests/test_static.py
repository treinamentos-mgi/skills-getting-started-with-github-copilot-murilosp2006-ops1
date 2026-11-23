def test_root_redirects_to_static_index(client):
    # Arrange
    target = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == target


def test_static_files_are_served_with_no_cache(client):
    # Arrange
    path = "/static/app.js"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-cache"


def test_api_responses_do_not_set_no_cache(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert "cache-control" not in response.headers
