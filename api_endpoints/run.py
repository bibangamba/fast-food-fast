# /run.py
import os

# from src import create_app #refers to create_app inside __init__.py
from src.app import create_app #refers to create_app inside app.py

# use below command to set flask_env instead of set
# $env:FLASK_ENV = "development"

if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV')
    # print(env_name)
    app = create_app(env_name)
    app.run()
