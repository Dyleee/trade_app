from pymongo import MongoClient
import hashlib
import os
from REST_api.core.errors import Responses

from REST_api.core.models import User

DEPOSITS = "deposit"
WITHDRAWALS = "withdrawals"


class DBClient:

    """
    Initiates the DB and holds DB-related methods
    """

    def __init__(self):
        client = MongoClient()
        self.db = client.database

    def create_user(self, form: dict):
        """
        Creates a User entry in the users Database.
        
        """

        # Check if user already exists:
        exists = User.objects.get(username = form['username'])
        if exists:
            return Responses.CONFLICT

        new_user = User(
            **form
        )
        new_user.save()
        return Responses.SUCCESS

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
