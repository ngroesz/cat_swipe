from web_service.database import db
from web_service.models.user import User


def authenticate_with_username_and_password(username, password):
    user = db.session.query(User).filter_by(username=username).filter_by(password=password).first()
    if user:
        return user
    else:
        return None
