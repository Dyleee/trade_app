from datetime import datetime
from REST_api.core.errors import Responses

from REST_api.core.models import User


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

        user = User.objects.get(username=query["username"])
        if not user:
            return Responses.INVALID_CREDENTIALS

        authorized = user.verify_password(query["password"])

        if not authorized:
            return Responses.INVALID_CREDENTIALS

        expiry = datetime.timedelta(day=5)
        access_token = user.generate_access_token(expiry)

        return 200, access_token

    def sign_up(self, *args, **kwargs) -> None:
        return self.app.db.create_user(*args, **kwargs)

    def login(self, *args, **kwargs) -> bool:
        self._verify_key(*args, **kwargs)
