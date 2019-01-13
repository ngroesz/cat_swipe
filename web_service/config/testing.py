import os
from dotenv import load_dotenv

load_dotenv()

PRESERVE_CONTEXT_ON_EXCEPTION = False
TESTING = True
FLASK_DEBUG = 0

SQLALCHEMY_ECHO = False

DATABASE_USERNAME = os.getenv('TEST_DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('TEST_DATABASE_PASSWORD')
DATABASE_HOSTNAME = os.getenv('TEST_DATABASE_HOSTNAME')
DATABASE_PORT = os.getenv('TEST_DATABASE_PORT')
DATABASE_NAME = os.getenv('TEST_DATABASE_NAME')

SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
    username=os.getenv('TEST_DATABASE_USERNAME'),
    password=os.getenv('TEST_DATABASE_PASSWORD'),
    host=os.getenv('TEST_DATABASE_HOSTNAME'),
    port=os.getenv('TEST_DATABASE_PORT'),
    database=os.getenv('TEST_DATABASE_NAME')
)
