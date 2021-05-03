from typing import Tuple

import flask

api: flask.Blueprint = flask.Blueprint("api", __name__, url_prefix="/api/v1")

@api.route("/health", methods=["GET"])
def health() -> Tuple[flask.Response, int]:
    """
    A simple sanity check to ensure that the API is reachable and working as expected.

    :return: JSON response and status code
    """
    return flask.jsonify(health="OK"), 200
