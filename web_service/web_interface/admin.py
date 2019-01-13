from flask import Blueprint, current_app, redirect, render_template, request, make_response, url_for
from flask_jwt_extended import jwt_required

from web_service.database import db, safe_add_object
from web_service.lib.app_config import value_for_key
from web_service.lib.common import format_json
from web_service.lib.configuration import load_data_types
from web_service.models.app_config import AppConfig
from web_service.models.contact import Contact
from web_service.models.data_type import DataType
from web_service.models.user import User
from web_service.lib.version import version_string
from web_service.web_interface.forms.contact_form import ContactForm
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


@bp.route('contacts')
@jwt_required
def contacts():
    return render_template('admin/contacts.html', title='Contact List')


@bp.route('contact_admin', methods=['GET', 'POST'])
@jwt_required
def contact_admin():
    contact_id = request.args.get('contact_id')
    new_contact = None
    contact = None
    if contact_id:
        contact = Contact.query.get(contact_id)
        new_contact = False
    else:
        contact = Contact()
        new_contact = True

    form = ContactForm(obj=contact)

    if new_contact:
        form.__delitem__('id')

    if form.validate_on_submit():
        form.populate_obj(contact)
        safe_add_object(contact)
        return make_response(redirect(url_for('admin.contacts')))

    return render_template('admin/contact_admin.html', title='Contact Admin', contact=contact, form=form)


@bp.route('alerts')
@jwt_required
def alerts():
    return render_template('admin/alerts.html', title='Alert List')


@bp.route('app_config', methods=['GET', 'POST'])
@jwt_required
def app_config():
    data_types = load_data_types()

    # This is done in a somewhat weird way since the app_config row with key == 'enable_daily_dose' may
    # or may not exist. We want there to exist no more than one rows with that key value.
    if request.method == 'POST':
        enable_daily_dose = db.session.query(AppConfig).filter_by(key='enable_daily_dose').first()
        enable_daily_dose = enable_daily_dose or AppConfig(key='enable_daily_dose')
        if request.form.get('enable_daily_dose_checkbox') and request.form.get('enable_daily_dose_checkbox') == 'on':
            enable_daily_dose.value = format_json('true')
        else:
            enable_daily_dose.value = format_json('false')
        db.session.add(enable_daily_dose)
        db.session.commit()

    return render_template(
               'admin/app_config.html',
               title='App Config',
               data_types=data_types,
               dashboard_config_value=value_for_key('dashboard_config') or [],
               daily_dose_is_enabled=value_for_key('enable_daily_dose'),
               version_string=version_string()
           )


@bp.route('dashboard_config_admin', methods=['GET', 'POST'])
@jwt_required
def dashboard_config_admin():
    dashboard_config = db.session.query(AppConfig).filter_by(key='dashboard_config').first()

    # Similar to the 'enable_daily_dose' logic elsewhere in this module, we want only one
    # app_config row with key == 'dashboard_config'
    if request.method == 'POST':
        dashboard_config = dashboard_config or AppConfig(key='dashboard_config')
        dashboard_config.value = format_json(request.form.get('dashboard_config'))
        db.session.add(dashboard_config)
        db.session.commit()

        return make_response(redirect(url_for('admin.app_config')))
    else:
        dashboard_config_value = ''
        if dashboard_config and dashboard_config.value:
            dashboard_config_value = dashboard_config.value
        else:
            dashboard_config_value = []

        return render_template(
                    'admin/dashboard_config_admin.html',
                    title='Dashboard Config',
                    dashboard_config_value=dashboard_config_value
               )


@bp.route('data_type_admin', methods=['GET', 'POST'])
@jwt_required
def data_type_admin():
    if request.args.get('delete_data_type'):
        type_name = request.args.get('data_type_name')
        current_app.logger.info('Deleting data-type {}'.format(type_name))
        data_type = db.session.query(DataType).filter_by(name=type_name).one()
        if data_type:
            db.session.delete(data_type)
            db.session.commit()

        return make_response(redirect(url_for('admin.app_config')))

    if request.method == 'POST':
        if request.form.get('data_type_name'):
            type_name = request.form.get('data_type_name')
            type_type = request.form.get('data_type_type')
            current_app.logger.info('Add data-type name: {}, type: {}'.format(type_name, type_type))
            existing_data_type = db.session.query(DataType).filter_by(name=type_name).first()
            if existing_data_type:
                current_app.logger.info('Type already exists, skipping')
            else:
                data_type = DataType(name=type_name, type=type_type)
                safe_add_object(data_type)

        return make_response(redirect(url_for('admin.app_config')))
    else:
        return render_template('admin/data_type_admin.html', title='Add Data Type')
