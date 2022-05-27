from flask_classful import FlaskView
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from REST_api.core.utils import TXNUtils



from .base import app


class TransactionsView(FlaskView):
    route_base: str = "transactions"
    default_methods: list  = ["POST"]
    NOWPAYMENTS_API: str = app.config["NOWPAYMENTS_API"]
    txn_utils = TXNUtils(app=app)

    auth_headers = {
        "x-api-key": app.config["NOWPAYMENTS_KEY"],
        "Content-Type": "application/json",
    }

    def index(self):
        return 200, "Transactions"

    @route("/create", methods=["POST"])
    def create(self):
        status, response = self.txn_utils.create_transaction(**request.form)
        return jsonify(status=status, message=response)
