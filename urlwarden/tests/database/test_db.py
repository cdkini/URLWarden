from datetime import datetime

import mongomock
import pytest

from urlwarden.database.db import MongoDatabase


@pytest.fixture
def mock_mongodb():
    """ Instantiates MongoDB database and fills with test data """
    conn = mongomock.MongoClient()
    objects = [
        {
            "_id": "user_1",
            "name": "User1",
            "email": "user1@email.com",
            "password": "password",
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
            "password": "password",
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "urls": [],
        },
    ]
    conn.db.users.insert(objects)
    mock_db = MongoDatabase(conn)
    return mock_db


def test_add_url_to_valid_user(mock_mongodb):
    assert mock_mongodb.add_url("user_2", "www.google.com", "def456") == None


def test_add_url_to_invalid_user(mock_mongodb):
    with pytest.raises(Exception):
        mock_mongodb.add_url("fake_user", "www.google.com", "def456")


def test_get_existant_url(mock_mongodb):
    assert mock_mongodb.get_url("abc123") == "www.google.com"


def test_get_nonexistant_url(mock_mongodb):
    with pytest.raises(Exception):
        mock_mongodb.get_url("fake_url")


def test_user_exists(mock_mongodb):
    assert mock_mongodb.user_exists("user1@email.com") == True


def test_user_not_exists(mock_mongodb):
    """ Should """
    assert mock_mongodb.user_exists("fake@email.com") == False
