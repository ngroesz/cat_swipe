"""
This file sets up a Flask application, using a factory method.
"""

from flask import Flask
from flask_jsglue import JSGlue
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
import os
import logging

from web_service.config import configure_app
from web_service.database import db
from web_service.lib.templates import get_arguments_for_all_templates

jwt = JWTManager()
socketio = SocketIO()
jsglue = JSGlue()


def create_app(config_name=None):
    flask_app = Flask(__name__)

    if not flask_app.debug:
        flask_app.logger.addHandler(logging.StreamHandler())
        flask_app.logger.setLevel(logging.INFO)

    configure_app(flask_app)

    db.init_app(flask_app)

    with flask_app.app_context():
        from web_service.api.bootstrap import api_bp # noqa
        flask_app.register_blueprint(api_bp)

    from web_service.auth import auth # noqa
    flask_app.register_blueprint(auth.bp, url_prefix='/')

    from web_service.web_interface import landing_page # noqa
    flask_app.register_blueprint(landing_page.bp, url_prefix='/')

    from web_service.web_interface import login # noqa
    flask_app.register_blueprint(login.bp, url_prefix='/login')

    from web_service.web_socket import pg_pubsub_client # noqa
    flask_app.register_blueprint(pg_pubsub_client.bp)

    jwt.init_app(flask_app)
    socketio.init_app(flask_app)
    jsglue.init_app(flask_app)

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @flask_app.context_processor
    def add_arguments_for_all_templates():
        return get_arguments_for_all_templates()

    flask_app.logger.info('created app with environment {}'.format(os.getenv('FLASK_ENV')))

    return flask_app
