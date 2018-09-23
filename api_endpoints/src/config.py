# /src/config.py

import os


class Development(object):
    """
    DEV environment config
    """
    DEBUG = True
    TESTING = False


class Production(object):
    """
    PROD environment config
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': Development,
    'production': Production,
}
