import datetime
import uuid
from REST_api.core.errors import Responses
from REST_api.core.models import Pool, Transactions, Users
import ujson
import requests


class Utils:

    """
    Holds utility methods like handling the SSO flow, verifying transactions...
    """

    def __init__(self, app):
        self.app = app

    def _verify_key(self, query: dict) -> None:
        """
        This will verify if the credentials exist and is are correct.
        If Credentials are valid then return Authorization Token to the App.
        """

        user = Users.objects.get(username=query["username"])
        if not user:
            return Responses.INVALID_CREDENTIALS

        authorized = user.verify_password(query["password"])

        if not authorized:
            return Responses.INVALID_CREDENTIALS

        expiry = datetime.timedelta(days=5)
        access_token = user.generate_access_token(expiry)

        return Responses.SUCCESS[0], access_token

    def sign_up(self, *args, **kwargs) -> None:
        return self.app.db.create_user(*args, **kwargs)

    def login(self, *args, **kwargs):
        return self._verify_key(*args, **kwargs)


class TXNUtils:
    def __init__(self, app) -> None:
        self.app = app
        self.NOWPAYMENTS_API: str = app.config["NOWPAYMENTS_API"]

        self.auth_headers = {
            "x-api-key": app.config["NOWPAYMENTS_KEY"],
            "Content-Type": "application/json",
        }
        self.DEPOSIT = "DEPOSIT"
        self.WITHDRAWAL = "WITHDRAWAL"
        self.TRADE = "TRADE"
        self.UNTRADE = "UNTRADE"

    def create_transaction(self, username: str, amount: int, type: str, days: int):
        match type.upper():
            case self.DEPOSIT:
                return self.create_pay_addr(username, amount)
            case self.WITHDRAWAL:
                return self.create_withdrawal(username, amount)
            case self.TRADE:
                return self.trade(username, amount, days)
            case _:
                return Responses.NOT_FOUND

    def create_withdrawal(self, username: str, amount: int):
        ...

    def trade(self, username: str, amount: int, days: int):
        # TODO
        """
        Creates a Trade Object and registers it in the Pool.
            :params username
            :params amount
        """
        user_information = self.app.db.fetch_txns_information(username)

        "If the user does not have enough."
        if user_information['balance'] < amount:
            return Responses.INVALID_CREDENTIALS

        payload = {
            "username": username,
            "amount": amount,
            "expiry_date": datetime.datetime.utcnow() + datetime.timedelta(days=days)
        }
        new_txn = Pool(**payload)
        new_txn.save()
        return Responses.CREATED
    
    def untrade(self, username: str, amount: int):
        ...

    def generate_address(self, pay_address):
        response = requests.get(
            f"https://api.cryptapi.io/trc20/usdt/qrcode/?address={pay_address}"
        )
        qr_code = response.json()["qr_code"]
        return {"address": pay_address, "qr_code": qr_code}

    def register_payment(self, username: str, type: str, nowpayments_response: dict):
        """
        Registers the payment to the assigned User as pending.
        """
        payload = {
            "txn_id": nowpayments_response["order_id"],
            "payment_id": nowpayments_response["order_id"],
            "username": username,
            "type": type,
            "datetime": datetime.now(),
            "status": nowpayments_response["payment_status"],
            "amount": nowpayments_response["price_amount"],
            "address": nowpayments_response["pay_address"],
        }

        new_txn = Transactions(**payload)
        new_txn.save()
        return Responses.CREATED

    def create_pay_addr(self, username: str, amount: int):
        """
        Create Payment Address and QR to be sent back to the client
            :params username
            :params amount
        """
        # exists = Transactions.objects.filter(username=username)
        # if exists:
        #     return Responses.CONFLICT
        exists = Transactions.objects.pending(username=username)
        if exists:
            return Responses.CONFLICT
        payload = ujson.dumps(
            {
                "price_amount": amount,
                "price_currency": "usd",
                "pay_amount": amount,
                "pay_currency": "usdttrc20",
                "order_description": "Rapidex OTC Deposit.",
                "order_id": uuid.uuid4().hex.upper()[0:15],
            },
            indent=4,
        )
        response = requests.post(
            self.NOWPAYMENTS_API, data=payload, headers=self.auth_headers
        ).json()

        print(response)

        # If we get a valid address, send the address and QR code to the client and register the payment to the database.
        if "pay_address" in response:
            address_and_qr = self.generate_address(response["pay_address"])
            self.register_payment(
                username=username, type="deposit", nowpayments_response=response
            )
            return Responses.CREATED[0], address_and_qr
        else:
            return Responses.INVALID_CREDENTIALS

        #    https://api.cryptapi.io/trc20/usdt/qrcode/?address=TWKitx7dLjcAccuqY7idVejgWRDrMAKiqN
