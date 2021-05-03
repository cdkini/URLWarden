import flask

def test_post_url_without_auth(client):
    response: flask.Response = client.post("/api/v1/urls", json={"url":"google.com"})

    assert response.status_code == 401
    assert "error" in response.get_json()

def test_post_url_with_missing_args(client, mocker):
    mocker.patch("urlwarden.database.url.URL.add_url", return_value="abcde")
    with client.session_transaction() as sess:
        sess["user"] = "1"
    response: flask.Response = client.post("/api/v1/urls", json={})

    assert response.status_code == 403
    assert "error" in response.get_json()

def test_valid_post_url(client, mocker):
    mocker.patch("urlwarden.database.url.URL.add_url", return_value="abcde")
    with client.session_transaction() as sess:
        sess["user"] = "1"
    response: flask.Response = client.post("/api/v1/urls", json={"url": "www.google.com"})

    assert response.status_code == 200
    assert "url" in response.get_json()

def test_get_url_without_auth(client):
    encoding: str = "abcde"
    response: flask.Response = client.get(f"/api/v1/urls/{encoding}")

    assert response.status_code == 401
    assert "error" in response.get_json()

def test_valid_get_url(client, mocker):
    mocker.patch("urlwarden.database.url.URL.get_url", return_value="www.google.com")
    with client.session_transaction() as sess:
        sess["user"] = "1"
    encoding: str = "abcde"
    response: flask.Response = client.get(f"/api/v1/urls/{encoding}")

    assert response.status_code == 200
    assert "url" in response.get_json()
