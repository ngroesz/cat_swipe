from flask import Blueprint

from web_service.web_interface.study import study_list

bp = Blueprint('landing_page', __name__)


@bp.route('/')
@bp.route('/index')
@bp.route('/index.html')
def landing_page():
    return study_list()
