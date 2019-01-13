import os


def is_test():
    return os.getenv('FLASK_ENV') == 'test'


def is_development():
    return os.getenv('FLASK_ENV') == 'development'


def is_production():
    return os.getenv('FLASK_ENV') == 'production'
