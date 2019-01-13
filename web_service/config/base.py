import os
from datetime import timedelta

DEBUG = False
TESTING = False
SQLALCHEMY_ECHO = True
SECRET_KEY = os.getenv('SECRET_KEY')
WTF_CSRF_CHECK_DEFAULT = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = False

# flask-rest-jsonapi
ALLOW_DISABLE_PAGINATION = True
PAGE_SIZE = 30

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_SECRET_KEY = SECRET_KEY
JWT_COOKIE_SECURE = False
JWT_COOKIE_CSRF_PROTECT = False
JWT_TOKEN_LOCATION = ['cookies']
