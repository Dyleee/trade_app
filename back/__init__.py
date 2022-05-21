from flask import Flask, request

from back.core.utils import Utils
from .db import DBClient
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
    
    @route("/user", methods=["POST"])
    def user(self):
        return

app.run()