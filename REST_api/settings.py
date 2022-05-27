import os 

MONGODB_SETTINGS = {"db": "tradeapp", "host": os.getenv("MONGO_URI")}
SECRET_KEY = os.getenv("SECRET_KEY")
NOWPAYMENTS_API = os.getenv("NOWPAYMENTS_API")
NOWPAYMENTS_KEY = os.getenv("NOWPAYMENTS_KEY")