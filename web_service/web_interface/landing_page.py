from flask import Blueprint

bp = Blueprint('landing_page', __name__)


@bp.route('/')
@bp.route('/index')
@bp.route('/index.html')
def landing_page():
    pass
