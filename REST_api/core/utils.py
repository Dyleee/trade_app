import hashlib
import os
from random import SystemRandom

UNICODE_ASCII_CHARACTER_SET = (
    "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789"
)


class Utils:

    """
    Holds utility methods like handling the SSO flow, verifying transactions...
    """

    def __init__(self, app):
        self.app = app

    def _verify_key(self, query: dict) -> None:
        entry = self.app.db.users.find_one(query["username"])
        username, name, email, key, salt = (
            entry.get("username"),
            entry.get("name"),
            entry.get("email"),
            entry.get("key"),
            entry.get("salt"),
        )

        new_key = hashlib.pbkdf2_hmac(
            "sha256", query["password"].encode("utf-8"), salt, 100000
        )

        return key == new_key

    def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        """Generates a non-guessable OAuth token
        Tokens should not be guessable
        and entropy when generating the random characters is important. Which is
        why SystemRandom is used instead of the default random.choice method.
        """
        rand = SystemRandom()
        return "".join(rand.choice(chars) for x in range(length))

    def sign_up(self, *args, **kwargs) -> None:
        self.app.db.create_user(*args, **kwargs)

    def login(self, *args, **kwargs) -> bool:
        self._verify_key(*args, **kwargs)