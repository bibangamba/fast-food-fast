#app/app.py

import os
from flask import Flask

from .config import app_config
from .views import order_api as order_blueprint
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)



def create_app(env_name):
    """    
    CREATE APP
    """
    #initialization
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')
    JWTManager(app)
    # jwt.init_app(APP)

    app.register_blueprint(order_blueprint, url_prefix='/api/v2/')
    
    return app
