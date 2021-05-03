import flask

def test_api_health(client):
    response: flask.Response = client.get("api/v1/health")

    assert response.json == {"health": "OK"} and response.status_code == 200
