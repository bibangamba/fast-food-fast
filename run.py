# /run.py
import os

from app.app import create_app
from app import APP

from app.db_helper import DatabaseConnectionHelper

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
APP.config = app.config
if __name__ == '__main__':
    port = os.getenv('PORT')
    app.run(host='127.0.0.1', port=port)

    db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
    db.create_all_tables()
    # delete the instance and hence close the connection and cursor
    del db
