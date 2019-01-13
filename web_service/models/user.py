from sqlalchemy import Boolean, Column, Integer, Text
from sqlalchemy.orm import deferred

from web_service.database.types import PasswordType

from web_service.database import db


class User(db.Model):
    __tablename__ = 'users'

    id           = Column(Integer, primary_key=True)
    username     = Column(Text, unique=True, nullable=False)
    password     = deferred(Column("password_hashed", PasswordType, nullable=False))
    email        = Column(Text)
    is_admin     = Column(Boolean, default=False)
    date_created = Column(db.DateTime(timezone=True))
    date_updated = Column(db.DateTime(timezone=True))

    def __repr__(self):
        return "<User %r>" % self.username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)
