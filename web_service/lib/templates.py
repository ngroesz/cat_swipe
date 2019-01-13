from flask_jwt_extended import get_current_user


def get_arguments_for_all_templates():
    return dict(current_user=get_current_user())
