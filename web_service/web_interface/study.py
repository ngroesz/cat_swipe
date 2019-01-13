from flask import Blueprint, render_template, request
from flask_jwt_extended import get_current_user, jwt_required

from web_service.lib.configuration import load_dashboard_config

bp = Blueprint('study', __name__)


@bp.route('study_list')
@jwt_required
def study_list():
    return render_template('study/study_list.html', title='Study List', current_user=get_current_user())


@bp.route('study_dashboard')
@jwt_required
def study_dashboard():

    return render_template('study/study_dashboard.html',
                           title='Study Dashboard',
                           study_id=request.args.get('study_id'),
                           latest_data_values_config=load_dashboard_config(key='latest_data_values'),
                           chart_and_table_config=load_dashboard_config(key='charts_and_tables')
                           )
