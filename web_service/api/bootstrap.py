from flask import Blueprint, current_app
from flask import jsonify
from flask_rest_jsonapi import Api
from web_service.lib.errors import PermissionDenied

from web_service.api.permissions import permission_manager

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint=api_bp)
api.permission_manager(permission_manager)


@current_app.errorhandler(PermissionDenied)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
