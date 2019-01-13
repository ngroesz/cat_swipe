"""
Application configuration for different environments, using environment variables.
"""

import os


def configure_app(flask_app):
    config_directory = os.path.join(flask_app.root_path, 'config')

    flask_app.config.from_pyfile(os.path.join(config_directory, 'base.py'))
    if os.getenv('FLASK_ENV') == 'test':
        flask_app.config.from_pyfile(os.path.join(config_directory, 'testing.py'))
    elif os.getenv('FLASK_ENV') == 'development':
        flask_app.config.from_pyfile(os.path.join(config_directory, 'development.py'))
    elif os.getenv('FLASK_ENV') == 'production':
        flask_app.config.from_pyfile(os.path.join(config_directory, 'production.py'))
    else:
        raise Exception('Unknown environment \"{}\"'.format(os.getenv('FLASK_ENV')))

    flask_app.config['DATABASE_URI'] = 'postgresql://{username}:{password}@{host}/{database}'.format(
        username=flask_app.config['DATABASE_USERNAME'],
        password=flask_app.config['DATABASE_PASSWORD'],
        host=flask_app.config['DATABASE_HOSTNAME'],
        database=flask_app.config['DATABASE_NAME']
    )
