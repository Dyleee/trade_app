from email import message
from flask import Flask, request, jsonify

from REST_api.core.utils import Utils
from REST_api.db import DBClient

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_classful import FlaskView, route


app = Flask(__name__)


class MainView(FlaskView):
    route_base = "/"

    def __init__(
        self,
    ):
        self.app = app
        self.app.db = DBClient()
        self.app.utils = Utils()

    def index(self):
        return 200, "Test"

    @route("/sign-up", methods=["POST"])
    def signUp(self):
        """
        Initiate Sign-up, return 201 on success, else possible error message.
        """
        status, response = self.app.utils.sign_up(request.form)
        match status:
            case 201:
                return jsonify(status=status, message=response)
            case _:
                return jsonify(status=status, message=response)

    @route("/login", methods=["POST"])
    def login(self):
        """
        Initiate Login, return access_token on success, else possible error message.
        """
        status, response = self.app.utils.login(request.form)
        match status:
            case 200:
                return jsonify(status=status, access_token=response)
            case _:
                return jsonify(status=status, message=response)

    @route("/user/<username>", methods=["GET"])
    @jwt_required
    def user(self, username):
        # user_info = self.app.db.
        transactions = self.app.db.fetch_txns_information(username)
        return


app.run()

""" TODO: User info fetching and Transaction Protocols.
"""
