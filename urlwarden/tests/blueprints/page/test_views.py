import flask 


def test_home_page(client):
    response = client.get(flask.url_for("page.home"))
    assert response.status_code == 200


def test_terms_page(client):
    response = client.get(flask.url_for("page.terms"))
    assert response.status_code == 200


def test_privacy_page(client):
    response = client.get(flask.url_for("page.privacy"))
    assert response.status_code == 200


def test_myurls_page_without_session(client):
    response = client.get(flask.url_for("page.myurls"))
    assert response.status_code == 302


def test_myurls_page_with_session(client):
    with client.session_transaction() as sess:
        sess["user"] = "testUser"
    response = client.get(flask.url_for("page.myurls"))
    assert response.status_code == 200


def test_login_page(client):
    response = client.get(flask.url_for("page.login"))
    assert response.status_code == 200
