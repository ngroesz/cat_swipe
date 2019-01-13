from flask_rest_jsonapi import ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

from web_service.api.bootstrap import api
from web_service.database import db
from web_service.models.swipe import Swipe


class SwipeSchema(Schema):
    id        = fields.Integer(required=True, dump_only=True)
    age       = fields.Integer()
    person_id = fields.Integer(required=True)

    class Meta:
        type_ = 'swipe'
        self_view = 'api.swipe'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.swipe_list'


class SwipeDetailApi(ResourceDetail):
    decorators = (api.has_permission(access_level='user'),)
    schema = SwipeSchema


class SwipeListApi(ResourceList):
    decorators = (api.has_permission(access_level='user'),)
    schema = SwipeSchema
    data_layer = {'session': db.session, 'model': Swipe}
