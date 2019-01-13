import eventlet
import json
import pgpubsub
import re
from flask import Blueprint

from web_service import create_app, socketio
from web_service.config import configure_app

eventlet.monkey_patch()

bp = Blueprint('pg_pubsub_client', __name__)

flask_app = create_app()


@bp.before_app_first_request
def start_listener():
    eventlet.spawn(pg_listen_thread)


def pg_listen_thread():
    with flask_app.app_context():
        configure_app(flask_app)
        pubsub = pgpubsub.connect(
                    dbname=flask_app.config['DATABASE_NAME'],
                    user=flask_app.config['DATABASE_USERNAME'],
                    password=flask_app.config['DATABASE_PASSWORD'],
                    host=flask_app.config['DATABASE_HOSTNAME'],
                    port=flask_app.config['DATABASE_PORT']
                 )
        pubsub.listen('table_update')
        while True:
            for event in pubsub.events(yield_timeouts=True):
                if event is None:
                    pass
                elif event.channel == 'table_update':
                    process_table_update(event)


def process_table_update(event):
    flask_app.logger.debug('process_message: {}'.format(event))
    table_update = json.loads(event.payload)
    with flask_app.app_context():
        socketio.emit(
            'table_update',
            {'table': table_name_from_fully_qualified_name(table_update['table_name']),
            'study_id': table_update['row']['study_id']},
            namespace='/browser'
        )


def table_name_from_fully_qualified_name(fully_qualified_name):
    match = re.search(r'[^\.]\.(.+)$', fully_qualified_name)

    if match:
        return match.group(1)

    return fully_qualified_name
