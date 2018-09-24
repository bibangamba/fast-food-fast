
# from flask import Flask

# from .config import app_config

# def create_app(env_name):
#     """    
#     CREATE APP
#     """
#     #initialization
#     app = Flask(__name__)
#     app.config.from_object(app_config[env_name])

#     @app.route('/', methods=['GET'])
#     def index():
#         """
#         sample endpoint
#         """
#         return "Hello world from an api endpoint!"

#     return app