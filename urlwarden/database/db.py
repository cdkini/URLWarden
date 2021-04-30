from abc import ABC, abstractmethod
from typing import Dict, Union

import flask
from flask_pymongo import PyMongo

from urlwarden.database.models import URLDocument, UserDocument

class Database(ABC):
    """ Defines the behavior that a database should adhere to in the context of the application. """
    @abstractmethod
    def init_app(self, app: flask.Flask):
        pass

    @abstractmethod
    def add_url(self, user_id: str, url: str, encoding: str):
        pass

    @abstractmethod
    def get_url(self, id: str):
        pass

    @abstractmethod
    def user_exists(self, email: str):
        pass

    @abstractmethod
    def add_user(self, email: str):
        pass


class MongoDatabase(Database):
    def __init__(self, conn: PyMongo):
        self.conn = conn

    def init_app(self, app: flask.Flask) -> None:
        """
        Initializes the database connection with the Flask app akin to other extensions.

        :param app: The Flask app

        :return: None
        """
        self.conn.init_app(app)

    def add_url(self, user_id: str, url: str, encoding: str) -> None:
        """
        Adds a URL, including its encoding, in the database.

        :param user_id: The requestor of the URL
        :param url: The full URL
        :param encoding: The hashed version of the full URL

        :raise Exception: If the requestor is not valid or authorized

        :return: None
        """
        url_doc: URLDocument = URLDocument(encoding, url)
        if not self.conn.db.users.find_one_and_update({"_id": user_id}, {"$push": {"urls": url_doc.jsonify()}}):
            raise Exception("Could not find user in database")

    def get_url(self, encoding: str) -> str:
        """
        Retrieves the full URL mapped to an encoded URL.

        :param encoding: The hash used to identify the URL

        :raise Exception: If the requested URL does not exist

        :return: Full URL corresponding to encoding
        """
        user_doc: Union[Dict, None] = self.conn.db.users.find_one(
            {"urls._id": encoding}, {"urls.url": 1, "_id": 0}
        )
        if not user_doc:
            raise Exception("Could not find user in database")
        return user_doc["urls"][0]["url"]

    def user_exists(self, email: str) -> bool:
        """
        Identifies whether or not a user is already in the system based on their email.

        :param email: The user's email

        :return: True if a valid user else False
        """
        return bool(self.conn.db.users.find_one({"email": email}))

    def add_user(self, name: str, email: str, password: str):
        """
        Adds a user to the database.
        
        :param name: Name of the user
        :param email: Email of the user
        :param password: Password of the email (encrypted before stored in the database)

        :raise Exception: If the database query fails for some reason

        :return: None
        """
        user_doc: UserDocument = UserDocument(name, email, password)
        if not self.conn.db.users.insert_one(user_doc):
            raise Exception("Something went wrong when inserting new user document")


db = MongoDatabase(PyMongo())
