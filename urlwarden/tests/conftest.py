from datetime import datetime

import mongomock
import pytest
from passlib.hash import pbkdf2_sha256
from urlwarden.database.db import DB

from urlwarden.app import create_app


@pytest.fixture(scope="session")
def app():
    """
    Setup our Flask test app (this only gets executed once)

    :return: Flask app
    """
    params = {
        "DEBUG": False,
        "TESTING": True,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    with _app.app_context():
        yield _app


@pytest.fixture(scope="function")
def client(app):
    """
    Setup our app client (this gets executed once for each test function)

    :param app: Pytest fixture
    :return: Flask app client
    """

    yield app.test_client()


@pytest.fixture(scope="function")
def db(app):
    mongo = mongomock.MongoClient()
    objects = [
        {
            "_id": "user_1",
            "name": "User1",
            "email": "user1@email.com",
            "password": pbkdf2_sha256.hash("password"),
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "urls": [
                {
                    "_id": "abc123",
                    "url": "www.google.com",
                    "created_at": datetime.utcnow(),
                    "expires_on": None,
                }
            ],
        },
        {
            "_id": "user_2",
            "name": "User2",
            "email": "user2@email.com",
            "password": pbkdf2_sha256.hash("password"),
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "urls": [],
        },
    ]
    mongo.db.users.insert_many(objects)
    return DB(mongo)

