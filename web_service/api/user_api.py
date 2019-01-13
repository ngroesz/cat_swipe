from flask_rest_jsonapi import ResourceList, ResourceDetail
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

from web_service.api.bootstrap import api
from web_service.database import db
from web_service.models.user import User


class UserSchema(Schema):
    id       = fields.Str(required=True, dump_only=True)
    username = fields.String()
    email    = fields.String()
    password = fields.String()
    is_admin = fields.Boolean()

    class Meta:
        type_ = 'user'
        self_view = 'api.user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.user_list'


class UserDetailApi(ResourceDetail):
    decorators = (api.has_permission(access_level='admin'),)
    schema = UserSchema
    data_layer = {'session': db.session, 'model': User}


class UserListApi(ResourceList):
    def after_get(self, result):
        for item in result['data']:
            del item['attributes']['password']
        return result

    decorators = (api.has_permission(access_level='admin'),)
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User,
                  'methods': {'after_get': after_get}}
