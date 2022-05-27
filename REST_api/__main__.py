from flask_jwt_extended import jwt_manager
from REST_api.core.models import mongo_engine

from REST_api.views.base import BaseView, app
from REST_api.views.transactions import TransactionsView

if __name__ == "__main__":
    # Register the routes
    BaseView.register(app, route_base="/")
    TransactionsView.register(app, route_base='transactions')

    # Initialize the JWT Manager
    jwt = jwt_manager.JWTManager(app=app)

    # Initialize Mongo Engine
    mongo_engine.init_app(app=app)
    print(app.url_map)
    app.run(port=10010, debug=True)