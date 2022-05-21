from flask import Flask, request

from REST_api.core.utils import Utils
from REST_api.db import DBClient

from flask_classful import FlaskView, route


app = Flask(__name__)

class MainView(FlaskView):
    route_base='/'

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
        self.app.utils.sign_up(request.form)
        return 200, "Success"

    @route("/login", methods=["POST"])
    def login(self):
        return 200, self.app.utils.login(request.form)
    
    @route("/user/<username>", methods=["GET"])
    def user(self, username):
        # user_info = self.app.db.
        transactions = self.app.db.fetch_txns_information(username)
        return

app.run()

""" TODO: Implement Handshake Protocols
User info fetching

"""