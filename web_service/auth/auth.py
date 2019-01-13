from flask import Blueprint, jsonify, redirect, request, make_response, url_for
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from web_service.database import db
from web_service.web_interface.login import login_page
from web_service import jwt
from web_service.lib.authentication import authenticate_with_username_and_password
from web_service.lib.common import ua_is_browser
from web_service.models.user import User

bp = Blueprint('auth', __name__)


@jwt.user_loader_callback_loader
def user_from_identity(identity):
    return db.session.query(User).filter_by(username=identity['id']).first()


@jwt.expired_token_loader
def expired_token_loader():
    response = None
    if ua_is_browser():
        return login_page()
    else:
        response = jsonify({
            'status': 401,
            'sub_status': 42,
            'msg': 'The token has expired'
        }), 401
    return response


@bp.route('/api/auth', methods=['POST'])
def api_login():
    username = request.json.get('device_id', None)
    password = request.json.get('password', None)

    user = authenticate_with_username_and_password(username, password)
    if user:
        identity = {'id': username, 'is_admin': user.is_admin}
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'login': False}), 401


@bp.route('/logout')
def logout():
    response = None
    if ua_is_browser:
        response = make_response(login_page())
    else:
        response = jsonify({'logout': True})

    unset_jwt_cookies(response)

    return response, 200


@jwt.unauthorized_loader
def unauthorized_loader(failed_user):
    response = None
    if ua_is_browser():
        response = make_response(redirect(url_for('login.login_page')))
    else:
        response = jsonify({'authorized': 'false'})
    return response
