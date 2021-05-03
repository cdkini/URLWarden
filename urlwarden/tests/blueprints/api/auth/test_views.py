import flask

def test_signup_with_missing_args(client, mocker):
    mocker.patch("urlwarden.database.user.User.user_exists", return_value=True)
    mocker.patch("urlwarden.database.user.User.add_user", return_value=True)
    response: flask.Response = client.post(
        "api/v1/auth/signup",
        json={
            "name": "User",
            "email": "user@email.com"
            # Missing password!
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_valid_signup(client, mocker):
    mocker.patch("urlwarden.database.user.User.user_exists", return_value=True)
    mocker.patch("urlwarden.database.user.User.add_user", return_value=True)
    response: flask.Response = client.post(
        "api/v1/auth/signup",
        json={
            "name": "User",
            "email": "user@email.com",
            "password": "password"
        },
    )

    assert response.status_code == 200
    assert "id" in response.get_json()


def test_login_with_missing_args(client, mocker):
    mocker.patch("urlwarden.database.user.User.authenticate_user",
                 return_value=True)
    response: flask.Response = client.post(
        "api/v1/auth/login",
        json={"email": "user@email.com"
              # Missing password!
              },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_valid_login(client, mocker):
    mocker.patch("urlwarden.database.user.User.authenticate_user", return_value=True)
    response: flask.Response = client.post(
        "api/v1/auth/login",
        json={
            "email": "user@email.com",
            "password": "password"
        },
    )

    assert response.status_code == 302


def test_logout(client):
    response: flask.Response = client.get("api/v1/auth/logout")

    assert response.status_code == 302
