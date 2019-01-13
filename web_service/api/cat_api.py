from flask_rest_jsonapi import ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

from web_service.api.bootstrap import api
from web_service.database import db
from web_service.models.cat import Cat


class CatSchema(Schema):
    id        = fields.Integer(required=True, dump_only=True)
    age       = fields.Integer()
    person_id = fields.Integer(required=True)

    class Meta:
        type_ = 'cat'
        self_view = 'api.cat'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.cat_list'


class CatDetailApi(ResourceDetail):
    decorators = (api.has_permission(access_level='user'),)
    schema = CatSchema


class CatListApi(ResourceList):
    decorators = (api.has_permission(access_level='user'),)
    schema = CatSchema
    data_layer = {'session': db.session, 'model': Cat}
