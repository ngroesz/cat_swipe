"""
In order to execute functions defined in this module, use the "flask"
command. You can type "flask shell" in order to get a shell context.
"""

from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
import click
import os
import simplejson as json

from web_service import create_app
from web_service import socketio
from web_service.database import db

from web_service.models.cat import Cat
from web_service.models.person import Person
from web_service.models.swipe import Swipe

dotenv_path = os.path.join('config', '.env')
load_dotenv(dotenv_path)

flask_app = create_app(os.getenv('FLASK_CONFIG') or None)

migrate = Migrate(flask_app, db)


@flask_app.shell_context_processor
def make_shell_context():
    return dict(app=flask_app, db=db,
                Cat=Cat,
                Person=Person,
                Swipe=Swipe)


@flask_app.cli.command()
def runserver():
    """Run the web-server."""
    from web_service.database import db_engine
    if not db_engine.dialect.has_table(db_engine, 'alembic_version'):
        initialize_database()
    else:
        upgrade()

    socketio.run(flask_app, host='0.0.0.0', port=5000, use_reloader=True)


@flask_app.cli.command()
@click.argument('username')
@click.argument('password')
@click.argument('is_admin')
def create_user(username, password, is_admin):
    """Create a user in the database."""
    from web_service.database import db
    is_admin = True if is_admin == '1' else False
    user = User(username=username, password=password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()


def initialize_database():
    upgrade()
    password = os.getenv('ADMIN_PASSWORD', 'CHANGEME')
    user = User(username='admin', password=password, is_admin=True)
    db.session.add(user)
    db.session.commit()
