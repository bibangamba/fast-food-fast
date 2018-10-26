# /run.py
import os
from flask import render_template
from app.app import create_app
from app import APP

from app.db_helper import DatabaseConnectionHelper

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
APP.config = app.config

db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
db.create_all_tables()
del db

@app.route("/")
@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signout")
def signout():
    return render_template('signout.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/orders")
def orders():
    return render_template('orders.html')

@app.route("/menu")
def menu():
    return render_template('menu.html')

# if the app is running in terminal (__main__) [__name__ is the app]
if __name__ == '__main__':
    port = os.getenv('PORT')
    app.run(host='127.0.0.1', port=port)
