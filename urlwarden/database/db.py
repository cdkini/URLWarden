from pymongo import MongoClient

from urlwarden.database.url import URL
from urlwarden.database.user import User


class DB:
    def __init__(self, mongo: MongoClient):
        self.__user: User = User(mongo)
        self.__url: URL = URL(mongo)

    @property
    def user(self):
        return self.__user

    @property
    def url(self):
        return self.__url


mongo: MongoClient = MongoClient()
db: DB = DB(mongo)
