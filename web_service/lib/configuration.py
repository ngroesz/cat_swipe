import simplejson as json

from web_service.database import db
from web_service.models.app_config import AppConfig
from web_service.models.data_type import DataType


def load_data_types():
    data_types = []
    for data_type in db.session.query(DataType).order_by(DataType.name).all():
        data_types.append({'name': data_type.name, 'type': data_type.type})

    return data_types


def load_dashboard_config(key=None):
    dashboard_config = db.session.query(AppConfig).filter_by(key='dashboard_config').first()
    if not dashboard_config or not dashboard_config.value:
        return []

    dashboard_json = json.loads(dashboard_config.value)
    if key is not None:
        if key in dashboard_json:
            return dashboard_json[key]
        else:
            return []

    return dashboard_json
