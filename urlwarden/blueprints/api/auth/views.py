from typing import Tuple, Union

import flask

auth: flask.Blueprint = flask.Blueprint("auth", __name__, url_prefix="/api/v1/auth")

from urlwarden.database.db import db


@auth.route("/signup", methods=["POST"])
def signup() -> Tuple[flask.Response, int]:
    """
    Allows a user to sign up for the service, adding user credentials and other relevant details
    to the database. Additionally, a session is created to signify that the user is now logged in.

    :return: JSON response and status code
    """
    json = flask.request.json
    name: Union[str, None] = json.get("name")
    email: Union[str, None] = json.get("email")
    password: Union[str, None] = json.get("password")
    if not name or not email or not password:
        return flask.jsonify(error="One of more required args is missing"), 400

    if not db.user.user_exists(email):
        return flask.jsonify(error="Email aready in use"), 400

    try:
        id: str = db.user.add_user(name, email, password)
    except Exception as e:
        return flask.jsonify(error=e), 400

    flask.session["user"] = id
    return flask.jsonify(id=id), 200


@auth.route("/login", methods=["POST"])
def login() -> Tuple[flask.Response, int]:
    """
    Authenticates a user and upon success, creates a user session.

    :return: JSON response and status code
    """
    json = flask.request.json
    email: Union[str, None] = json.get("email")
    password: Union[str, None] = json.get("password")
    if not email or not password:
        return flask.jsonify(error="One of more required args is missing"), 400

    try:
        id: str = db.user.authenticate_user(email, password)
    except Exception as e:
        return flask.jsonify(error=e), 400

    flask.session["user"] = id
    return flask.redirect("/", Response=flask.Response), 302


@auth.route("/logout", methods=["GET"])
def logout() -> Tuple[flask.Response, int]:
    """
    Logs user out by removing their session.

    :return: JSON response and status code
    """
    flask.session.pop("user", None)
    return flask.redirect("/", Response=flask.Response), 302
