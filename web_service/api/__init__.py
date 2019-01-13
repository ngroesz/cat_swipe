"""
The __init__.py file sets up routes for the API
Each API module also defines a schema.
The relevant modules are flask-rest-jsonapi and marshmallow-jsonapi
To see a list of route endpoints and URLs, do something like:
> flask routes
"""

from web_service.api.bootstrap import api

from web_service.api.alert_api import AlertDetailApi, AlertListApi
from web_service.api.app_config_api import AppConfigDetailApi, AppConfigListApi
from web_service.api.contact_api import ContactDetailApi, ContactListApi
from web_service.api.data_type_api import DataTypeDetailApi, DataTypeListApi
from web_service.api.latest_long_acting_insulin_setting_api import LatestLongActingInsulinSettingListApi
from web_service.api.latest_short_acting_insulin_setting_api import LatestShortActingInsulinSettingListApi
from web_service.api.latest_study_data_api import LatestStudyDataListApi
from web_service.api.long_acting_insulin_setting_api import LongActingInsulinSettingDetailApi, LongActingInsulinSettingListApi, LongActingInsulinSettingRelationship
from web_service.api.short_acting_insulin_setting_api import ShortActingInsulinSettingDetailApi, ShortActingInsulinSettingListApi, ShortActingInsulinSettingRelationship
from web_service.api.study_api import StudyDetailApi, StudyListApi
from web_service.api.study_data_api import StudyDataDetailApi, StudyDataListApi
from web_service.api.user_api import UserDetailApi, UserListApi

api.route(AlertDetailApi, 'alert_detail', '/alert')
api.route(AlertListApi, 'alert_list', '/alerts')

api.route(AppConfigDetailApi, 'app_config_detail', '/app_config/<int:id>')
api.route(AppConfigListApi, 'app_config_list', '/app_configs')

api.route(ContactDetailApi, 'contact_detail', '/contact')
api.route(ContactListApi, 'contact_list', '/contacts')

api.route(DataTypeDetailApi, 'data_type_detail', '/data_type')
api.route(DataTypeListApi, 'data_type_list', '/data_types')

api.route(LatestLongActingInsulinSettingListApi, 'latest_long_acting_insulin_setting_list', '/latest_long_acting_insulin_setting/<string:study_id>')

api.route(LatestShortActingInsulinSettingListApi, 'latest_short_acting_insulin_setting_list', '/latest_short_acting_insulin_setting/<string:study_id>')

api.route(LatestStudyDataListApi, 'latest_study_data_list', '/latest_study_data/<string:study_id>')

api.route(LongActingInsulinSettingDetailApi, 'long_acting_insulin_setting_detail', '/long_acting_insulin_setting/<int:id>')
api.route(LongActingInsulinSettingListApi, 'long_acting_insulin_setting_list', '/long_acting_insulin_settings', '/study/<string:study_id>/long_acting_insulin_settings')
api.route(LongActingInsulinSettingRelationship, 'long_acting_insulin_setting_study', '/long_acting_insulin_settings/<int:id>/relationships/study')

api.route(ShortActingInsulinSettingDetailApi, 'short_acting_insulin_setting_detail', '/short_acting_insulin_setting/<int:id>')
api.route(ShortActingInsulinSettingListApi, 'short_acting_insulin_setting_list', '/short_acting_insulin_settings', '/study/<string:study_id>/short_acting_insulin_settings')
api.route(ShortActingInsulinSettingRelationship, 'short_acting_insulin_setting_study', '/short_acting_insulin_settings/<int:id>/relationships/study')

api.route(StudyDataDetailApi, 'study_data_detail', '/study_data/<int:id>')
api.route(StudyDataListApi, 'study_data_list', '/study/<string:study_id>/data')

api.route(StudyDetailApi, 'study_detail', '/study/<string:id>')
api.route(StudyListApi, 'study_list', '/studies')

api.route(UserDetailApi, 'user_detail', '/user')
api.route(UserListApi, 'user_list', '/users')
