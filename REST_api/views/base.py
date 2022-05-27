from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route
from REST_api.core.utils import Utils
from REST_api.db_handler import DBClient

# Load environment variables
load_dotenv()

# Create App Instance and config DB
app = Flask(__name__)
app.config.from_pyfile("../settings.py")

# Create the Primary API view
class BaseView(FlaskView):
    app.db = DBClient()
    app.utils = Utils(app)

    @route("/", methods=["GET"])
    def index(self):
        return 200, "Test"

    @route("/sign-up", methods=["POST"])
    def signUp(self):
        """
        Initiate Sign-up, return 201 on success, else possible error message.
        """
        status, response = app.utils.sign_up(request.form)
        return jsonify(status=status, message=response)

    @route("/login", methods=["POST"])
    def login(self):
        """
        Initiate Login, return access_token on success, else possible error message.
        """
        status, response = app.utils.login(request.form)
        match status:
            case 200:
                return jsonify(status=status, access_token=response)
            case _:
                return jsonify(status=status, message=response)

    @jwt_required()
    @route("/user/<username>", methods=["GET"])
    def user(self, username):
        status, response = app.db.fetch_txns_information("dylee")
        return jsonify(status=status, message=response)

""" TODO: User info fetching and Transaction Protocols.
Crypto Instant Payment Flow
Invite Code Implementation (Team Feature)
"""
