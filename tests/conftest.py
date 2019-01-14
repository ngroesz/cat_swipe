from flask import _app_ctx_stack
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SessionBase
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, join, realpath
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import json
import os
import pytest

from fixtures.persons import create_persons
from fixtures.users import create_users
import web_service.database
#from web_service.database import connection_string, db, db_engine
from web_service import create_app

@pytest.yield_fixture(scope='function')
def _db():
    print('OPENING SESSION')
    web_service.database.db_engine = create_engine(web_service.database.connection_string(), echo=True)
    connection = web_service.database.db_engine.connect()
    transaction = connection.begin()
    web_service.database.db.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )

    print("created session: {}".format(web_service.database.db.session))

    yield web_service.database.db.session

    print('CLOSING SESSION')
    web_service.database.db.session.close()
    transaction.rollback()
    connection.close()
    web_service.database.db_engine.dispose()
    #del web_service.database.db_engine
    #del connection
    #del web_service.database.db.session


@pytest.yield_fixture(scope="function")
def flask_app(request):
    flask_app = create_app({'TESTING': True})
    context = flask_app.app_context()
    context.push()
    flask_app.debug = True

    yield flask_app

    context.pop()


@pytest.fixture(scope="function")
def client(_db, flask_app):
    yield flask_app.test_client()


@pytest.fixture(scope="function")
def authenticated_admin(client, create_users):
    identity = {'id': 'admin', 'is_admin': True}
    access_token = create_access_token(identity=identity)
    client.set_cookie('localhost', 'access_token_cookie', access_token)


@pytest.fixture(scope="function")
def authenticated_user(client, create_users):
    identity = {'id': '1234', 'is_admin': False}
    access_token = create_access_token(identity=identity)
    client.set_cookie('localhost', 'access_token_cookie', access_token)
