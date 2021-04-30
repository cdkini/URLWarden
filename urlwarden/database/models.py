import uuid
from datetime import datetime
from typing import List, Tuple, Union

import passlib.hash


class UserDocument: # pragma: no cover
    def __init__(self, name: str, email: str, password: str):
        self._id: Tuple[str] = uuid.uuid4().hex,
        self.name: str = name
        self.email: str = email
        self.password: str = passlib.pbkdf2_sha256.encrypt(password)
        self.created_at: datetime = datetime.utcnow()
        self.last_login: datetime = datetime.utcnow()
        self.urls: List[URLDocument] = []


class URLDocument: # pragma: no cover
    def __init__(self, url: str, encoding: str, expiration: datetime = None):
        self._id: str = encoding
        self.url: str = url
        self.created_at: datetime = datetime.utcnow()
        self.expires_on: Union[datetime, None] = expiration

    def jsonify(self):
        return self.__dict__
