# /run.py
import os

# from src import create_app #refers to create_app inside __init__.py
from src.app import create_app  # refers to create_app inside app.py

# use below command to set flask_env instead of set
# $env:FLASK_ENV = "development"

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
    port = os.getenv('PORT')
    # print(env_name)
    # app.run()
    app.run(host='0.0.0.0', port=port)
