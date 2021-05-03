from typing import Any, Mapping

import os
import flask

from urlwarden.blueprints.api import api
from urlwarden.blueprints.api.auth import auth
from urlwarden.blueprints.api.urls import urls
from urlwarden.blueprints.page import page
from urlwarden.extensions import cache, debug_toolbar, session


def create_app(settings_override: Mapping[str, Any] = None) -> flask.Flask:
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings (used when running tests)
    :return: Flask app
    """
    app: flask.Flask = flask.Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    if settings_override:
        app.config.update(settings_override)

    blueprints(app, api, urls, auth, page)
    extensions(app, debug_toolbar, cache, session)


    return app


def blueprints(app: flask.Flask, *blueprints: flask.Blueprint) -> None:
    """
    Register 0 or more blueprints (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def extensions(app: flask.Flask, *extensions: Any) -> None:
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    for extension in extensions:
        extension.init_app(app)
