from flask_jwt_extended import jwt_required, get_jwt_identity
from web_service.lib.errors import PermissionDenied


@jwt_required
def permission_manager(view, view_args, view_kwargs, *args, **kwargs):
    if 'access_level' in kwargs:
        identity = get_jwt_identity()

        if identity is None:
            raise PermissionDenied('Permission Denied', status_code=403)

        if kwargs['access_level'] == 'user':
            return
        elif kwargs['access_level'] == 'admin':
            if identity['is_admin']:
                return
            else:
                raise PermissionDenied('Permission Denied', status_code=403)

    raise PermissionDenied('Permission Denied', status_code=403)
