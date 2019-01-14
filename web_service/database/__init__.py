from flask import _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os


#
# this function is a work-around.
# I was having errors like "Object '<>' is already attached to session '1' (this is '2')"
# stackoverflow said that circular imports are to blame but I don't think that that is the case here?
def safe_add_object(object):
    current_db_session = db.session.object_session(object)

    if not current_db_session:
        current_db_session = db.session

    current_db_session.add(object)
    current_db_session.commit()


def create_db_engine():
    db_engine = create_engine(connection_string())
    return db_engine


def connection_string():
    # TODO: there is also a config file ... but i've had trouble getting the app_context working
    if os.getenv('FLASK_ENV') == 'test':
        username = os.getenv('TEST_DATABASE_USERNAME')
        password = os.getenv('TEST_DATABASE_PASSWORD')
        host     = os.getenv('TEST_DATABASE_HOSTNAME')
        database = os.getenv('TEST_DATABASE_NAME')
    elif os.getenv('FLASK_ENV') == 'development':
        username = os.getenv('DEVELOPMENT_DATABASE_USERNAME')
        password = os.getenv('DEVELOPMENT_DATABASE_PASSWORD')
        host     = os.getenv('DEVELOPMENT_DATABASE_HOSTNAME')
        database = os.getenv('DEVELOPMENT_DATABASE_NAME')
    elif os.getenv('FLASK_ENV') == 'production':
        username = os.getenv('PRODUCTION_DATABASE_USERNAME')
        password = os.getenv('PRODUCTION_DATABASE_PASSWORD')
        host     = os.getenv('PRODUCTION_DATABASE_HOSTNAME')
        database = os.getenv('PRODUCTION_DATABASE_NAME')
    else:
        raise Exception('Unrecognized environment {}'.format(os.getenv('FLASK_ENV')))

    return 'postgresql://{username}:{password}@{host}/{database}'.format(
        username=username,
        password=password,
        host=host,
        database=database
    )


db = SQLAlchemy()
base = declarative_base()
#should_echo = True if os.getenv('FLASK_ENV') == 'development' else False
#db_engine = create_engine(connection_string(), echo=should_echo)
#db.session = scoped_session(
#                sessionmaker(autocommit=False, autoflush=False, bind=db_engine),
#                scopefunc=_app_ctx_stack.__ident_func__
#             )
