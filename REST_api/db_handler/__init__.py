import ujson
from pymongo import MongoClient
from bson import json_util

from REST_api.core.errors import Responses

from REST_api.core.models import User
import os
import uuid

DEPOSITS = "deposits"
WITHDRAWALS = "withdrawals"


class DBClient:

    """
    Initiates the DB and holds DB-related methods
    """

    def __init__(self):
        client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = client.test

    def create_user(self, form: dict):
        """
        Creates a User entry in the users Database.

        """

        # Create Unique Invite code and Check if user already exists:
        invite_code = uuid.uuid4().hex.upper()[0:6]
        exists = User.objects.filter(username=form["username"])
        if exists:
            return Responses.CONFLICT

        new_user = User(invite_code=invite_code, **form)
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
            {"$match": {"username": "dyleee"}},
            {
                "$group": {
                    "_id": "$txn_id",
                    "username": {"$first": "$username"},
                    "txn_type": {"$first": "$txn_type"},
                    "balance": {"$sum": "$amount"},
                    "datetime": {"$first": "$datetime"},
                }
            },
        ]

        """
        The datetime Object will follow Python's datetime.datetime.now() object
        """
        cursor = self.db.transactions.aggregate(pipeline=pipeline)
        result = [entry for entry in cursor]
        if not result:
            return Responses.NOT_FOUND[0], "No Transactions found."
        return Responses.SUCCESS[0], result
