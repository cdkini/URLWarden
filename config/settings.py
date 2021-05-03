import os
import uuid

DEBUG = True

SERVER_NAME = "0.0.0.0:8000"
SESSION_TYPE = "filesystem"
SECRET_KEY = uuid.uuid4().hex 

MONGO_URI = os.environ.get("MONGO_URI")
