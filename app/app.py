#app/app.py

from flask import Flask

from .config import app_config
from .views import order_api as order_blueprint


def create_app(env_name):
    """    
    CREATE APP
    """
    #initialization
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders/')
    # app.register_blueprint(menu_blueprint, url_prefix='/api/v2/orders/')
    # app.register_blueprint(user_blueprint, url_prefix='/api/v2/orders/')
    
    return app
