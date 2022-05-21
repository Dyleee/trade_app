from pymongo import MongoClient
import hashlib
import os


class DBClient:
    def __init__(self):
        client = MongoClient()
        self.db = client.crypto_sprout

    def create_user(self, form):
        username, name, email, password = (
            form.get("username"),
            form.get("name"),
            form.get("email"),
            form.get("password"),
        )
        salt = os.urandom(32)

        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        entry = {
            "username": username,
            "name": name,
            "email": email,
            "key": key,
            "salt": salt,
        }

        self.db.users.insert_one(entry)
