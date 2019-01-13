"""
This package defines models which are used by SQLAlchemy. These model files are
the canonical schema definition. Alembic migrations are generated from these
modules.
This __init__.py file sets-up listening events with SQLAlchemy so that, say, the
date_created column will be set on new rows.
"""

from sqlalchemy import event
from datetime import datetime

from web_service.models.user import User


def set_creation_time(mapper, connection, target):
    target.date_created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def set_updated_time(mapper, connection, target):
    target.date_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")


event.listen(User, 'before_insert', set_creation_time)
event.listen(User, 'before_update', set_updated_time)
