import os 

MONGODB_SETTINGS = {"db": "tradeapp", "host": os.getenv("MONGO_URI")}
SECRET_KEY = os.getenv("SECRET_KEY")