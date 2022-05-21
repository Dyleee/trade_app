from pymongo import MongoClient
import hashlib
import os

DEPOSITS = "deposit"
WITHDRAWALS = "withdrawals"


class DBClient:
    def __init__(self):
        client = MongoClient ()
        self.db = client.database

    # TODO : Unit Testing

    def create_user(self, form):
        """
        Creates a User entry in the users Database.
        """
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
            "invite_code": f"{salt[5]}{username[:2]}{salt[3]}" 
        }

        self.db.users.insert_one(entry)

    def fetch_txns_information(self, username):
        """
        This returns all transactions in this format:
            [
                {"_id": transaction_id, "user": "username", "type": deposit/withdrawal, "balance": user_balance},
                ...
            ]
        """
        pipeline = [
            {"$match": {"username": username}},
            {
                "$group": {
                    "_id": "$txn_id",
                    "user": "username",
                    "type": "type",
                    "balance": {"$sum": "$amount"},
                    "datetime": "datetime"
                }
            },
        ]
        cursor = self.db.transactions.aggregate(pipeline=pipeline)
        return [entry for entry in cursor]
