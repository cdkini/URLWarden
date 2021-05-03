import hashlib
import re
from datetime import datetime
from typing import Any, Dict, List, Union

from pymongo import MongoClient


class URL:
    def __init__(self, mongo: MongoClient):
        self.__mongo = mongo

    def add_url(self, user_id: str, url: str) -> None:
        """
        Adds a URL, including its encoding, in the database.

        :param user_id: The requestor of the URL
        :param url: The full URL
        :param encoding: The hashed version of the full URL

        :raise Exception: If the requestor is not valid or authorized

        :return: None
        """
        encoding = URL._encode(user_id, url)
        url_doc: Dict[str, Any] = {
            "_id": encoding,
            "url": url,
            "created_at": datetime.utcnow(),
            "expiration": None,
        }
        if not self.__mongo.db.users.find_one_and_update(
            {"_id": user_id}, {"$push": {"urls": url_doc}}
        ):
            raise Exception("Could not find user in database")

    def get_url(self, encoding: str):
        """
        Retrieves the full URL mapped to an encoded URL.

        :param encoding: The hash used to identify the URL

        :raise Exception: If the requested URL does not exist

        :return: Full URL corresponding to encoding
        """
        user_doc: Union[Dict, None] = self.__mongo.db.users.find_one(
            {"urls._id": encoding}, {"urls.url": 1, "_id": 0}
        )
        if not user_doc:
            raise Exception("Could not find user in database")
        return user_doc["urls"][0]["url"]

    @staticmethod
    def _sanitize(url: str) -> str:
        r: re.Pattern[str] = re.compile(r"https?://(www\.)?")
        string: str = r.sub("", url).strip().strip("/")
        return string.replace("www.", "")

    @staticmethod
    def _encode(secret: str, url: str, encoding_length: int = 7) -> str:
        input: str = secret + "-" + url
        hash_obj: hashlib._Hash = hashlib.md5(str(input).encode("utf-8"))
        digest: str = hash_obj.hexdigest()

        val: int = int(digest, 16)
        base62: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        res: List[str] = []
        while val:
            char: str = base62[val % 62]
            res.append(char)
            val //= 62

        return "".join(r for r in res[:encoding_length])
