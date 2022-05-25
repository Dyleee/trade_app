import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_mongoengine import MongoEngine as mg

mongo_engine = mg()

class User(mongo_engine.Document):

    username = mongo_engine.StringField(unique=True, min_length=4)
    name = mongo_engine.StringField()
    email = mongo_engine.EmailField()
    password = mongo_engine.StringField(unique=True, min_length=6, regex=None)
    invite_code = mongo_engine.StringField(unique=True)

    def encrypt_password(self):
        self.password = generate_password_hash(password=self.password).decode("utf-8")

    encrypt_password.__doc__ = generate_password_hash.__doc__

    def verify_password(self, password: str):
        return check_password_hash(pw_hash=self.password, password=password)

    verify_password.__doc__ = check_password_hash.__doc__

    def generate_access_token(self, expiry: datetime.timedelta):
        return create_access_token(identity=self.username, expires_delta=expiry)

    def save(self, *args, **kwargs):
        if self._created:
            self.encrypt_password()
        super(User, self).save(*args, **kwargs)


class Transactions(mongo_engine.Document):
    txn_id = mongo_engine.StringField()
    username = mongo_engine.StringField()
    type = mongo_engine.StringField
    datetime = mongo_engine.DateTimeField(required=True)
