from . import app
from flask_jwt_extended import jwt_manager
from REST_api.core.models import mongo_engine

if __name__ == "__main__":
    jwt = jwt_manager.JWTManager(app=app)
    mongo_engine.init_app(app=app)
    app.run(port=10010, debug=True)