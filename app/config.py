# /app/config.py

import os
from dotenv import load_dotenv
load_dotenv()

class Development(object):
    """
    DEV environment config
    """
    DEBUG = True
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI')
    JWT_SECRET = os.getenv('JWT_SECRET')


class Production(object):
    """
    PROD environment config
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI')
    JWT_SECRET = os.getenv('JWT_SECRET')


class Testing(object):
    """
    DEV environment config
    """
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    JWT_SECRET = os.getenv('JWT_SECRET')


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
