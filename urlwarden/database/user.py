import uuid
from datetime import datetime
from typing import Any, Dict

from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient


class User:
    def __init__(self, mongo: MongoClient):
        self.__mongo = mongo

    def user_exists(self, email: str) -> bool:
        """
        Identifies whether or not a user is already in the system based on their email.

        :param email: The user's email

        :return: True if a valid user else False
        """
        return bool(self.__mongo.db.users.find_one({"email": email}))

    def authenticate_user(self, email: str, password: str):
        user_doc = self.__mongo.db.users.find_one(
            {"email": email}, {"password": pbkdf2_sha256.hash(password)}
        )
        if not user_doc:
            raise Exception("Something went wrong when inserting new user document")
        return user_doc.get("_id")

    def add_user(self, name: str, email: str, password: str):
        """
        Adds a user to the database.

        :param name: Name of the user
        :param email: Email of the user
        :param password: Password of the email (encrypted before stored in the database)

        :raise Exception: If the database query fails for some reason

        :return: None
        """
        id = uuid.uuid4().hex
        user_doc: Dict[str, Any] = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "email": email,
            "password": pbkdf2_sha256.hash(password),
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "urls": [],
        }
        if not self.__mongo.db.users.insert_one(user_doc):
            raise Exception("Something went wrong when inserting new user document")
        return id
