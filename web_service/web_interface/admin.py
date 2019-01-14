from flask import Blueprint, current_app, redirect, render_template, request, make_response, url_for
from flask_jwt_extended import jwt_required

from web_service.database import db, safe_add_object
from web_service.lib.common import format_json
from web_service.models.user import User
from web_service.lib.version import version_string
from web_service.web_interface.forms.user_form import UserForm

bp = Blueprint('admin', __name__)


@bp.route('users')
@jwt_required
def users():
    return render_template('admin/users.html', title='User List', users=User.query.all())


@bp.route('user_admin', methods=['GET', 'POST'])
@jwt_required
def user_admin():
    new_user = None
    user = None
    form = None
    if request.args.get('user_id'):
        user = User.query.get(request.args.get('user_id'))
        form = UserForm(obj=user)
        new_user = False
    else:
        form = UserForm()
        form.__delitem__('id')
        new_user = True

    if form.validate_on_submit():
        if new_user:
            user = User(username=form.data['username'], password=form.data['email'])

        user.username = form.data['username']
        user.email = form.data['email']
        user.is_admin = form.data['is_admin']

        # We want to avoid updating the password when the form password value is blank
        # There is probably a better way to do this.
        if form.data['password'] and len(form.data['password']) > 0:
            user.password = form.data['password']

        safe_add_object(user)

        return make_response(redirect(url_for('admin.users')))

    return render_template('admin/user_admin.html', title='User Admin', user=user, form=form)
