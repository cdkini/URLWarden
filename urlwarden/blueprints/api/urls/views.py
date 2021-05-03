import os
from typing import Tuple, Union

import flask

from urlwarden.database.db import db
from urlwarden.extensions import cache

urls: flask.Blueprint = flask.Blueprint("urls", __name__, url_prefix="/api/v1/urls")


@urls.route("", methods=["POST"])
def post_url() -> Tuple[flask.Response, int]:
    """
    Takes an input URL from the user and encodes it.
    Note that the hashed URL is added to both the cache and the database upon generation (unless it already exists).

    :return: JSON response and status code
    """
    user = flask.session.get("user")
    if not user:
        return flask.jsonify(error="User is not authenticated"), 401

    long_url: Union[str, None] = flask.request.json.get("url")
    if not long_url:
        return flask.jsonify(error="One or more required args is missing"), 403

    try:
        encoding = db.url.add_url(user, long_url)
    except Exception as e:
        return flask.jsonify(error=e), 400

    short_url: str = f"{os.environ.get('BASE_URL')}/{encoding}"

    cache.set(encoding, long_url)
    return flask.jsonify(url=short_url), 200


@urls.route("/<encoding>", methods=["GET"])
def get_url(encoding: str) -> Tuple[flask.Response, int]:
    """
    Takes an input encoding or hash from the user and decyphers it.
    Note that the hashed URL is added to both the cache and the database upon decyphering.

    :return: JSON response and status code
    """
    user = flask.session.get("user")
    if not user:
        return flask.jsonify(error="User is not authenticated"), 401

    if cache.get(encoding):
        url: str = cache.get(encoding)
        cache.set(encoding, url)  # Reset the cache TTL
        return flask.jsonify(url=url), 200

    try:
        url = db.url.get_url(encoding)
    except Exception as e:
        return flask.jsonify(error=e), 404

    cache.set(encoding, url)
    return flask.jsonify(url=url), 200
