import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_mongoengine import QuerySet, MongoEngine as mg

mongo_engine = mg()

class Users(mongo_engine.Document):
    username = mongo_engine.StringField(unique=True, min_length=4)
    name = mongo_engine.StringField()
    email = mongo_engine.EmailField()
    password = mongo_engine.StringField(unique=True, min_length=6, regex=None)
    invite_code = mongo_engine.StringField(unique=True)
    confirmed = mongo_engine.BooleanField(default=False)

    def verify_password(self, password: str):
        return check_password_hash(pw_hash=self.password, password=password)
    verify_password.__doc__ = check_password_hash.__doc__

    def encrypt_password(self):
        self.password = generate_password_hash(password=self.password).decode("utf-8")
    encrypt_password.__doc__ = generate_password_hash.__doc__

    def generate_access_token(self, expiry: datetime.timedelta):
        return create_access_token(identity=self.username, expires_delta=expiry)

    def save(self, *args, **kwargs):
        if self._created:
            self.encrypt_password()
        super(Users, self).save(*args, **kwargs)

class TXNsQuerySet(QuerySet):
    def pending(self, username: str):
        return self.filter(status="waiting", username=username)

class Transactions(mongo_engine.Document):
    meta = {"queryset_class": TXNsQuerySet}
    txn_id = mongo_engine.StringField()
    payment_id = mongo_engine.StringField()
    username = mongo_engine.StringField()
    type = mongo_engine.StringField()
    datetime = mongo_engine.DateTimeField(required=True)
    status = mongo_engine.StringField()
    amount = mongo_engine.IntField()
    address = mongo_engine.StringField()

class Pool(mongo_engine.Document):
    expiry_date = mongo_engine.DateTimeField()
    username = mongo_engine.StringField()
    amount = mongo_engine.IntField()