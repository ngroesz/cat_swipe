from flask import Blueprint, redirect, render_template, request, make_response, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies

from web_service.lib.authentication import authenticate_with_username_and_password

bp = Blueprint('login', __name__)


@bp.route('login_page', methods=['GET', 'POST'])
def login_page(error_msg=None):
    if request.method == 'POST' and not error_msg:
        username = request.form['username']
        password = request.form['password']

        user = authenticate_with_username_and_password(username, password)
        if user:
            identity = {'id': username, 'is_admin': user.is_admin}
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)

            response = make_response(redirect(url_for('study.study_list')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        else:
            return login_page(error_msg='Username or password incorrect')
    else:
        return render_template('login/login_page.html', error_msg=error_msg)
