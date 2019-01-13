from flask_rest_jsonapi import ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

from web_service.api.bootstrap import api
from web_service.database import db
from web_service.models.person import Person


class PersonSchema(Schema):
    id        = fields.Integer(required=True, dump_only=True)
    age       = fields.Integer()

    class Meta:
        type_ = 'person'
        self_view = 'api.person'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.person_list'


class PersonDetailApi(ResourceDetail):
    decorators = (api.has_permission(access_level='user'),)
    schema = PersonSchema


class PersonListApi(ResourceList):
    decorators = (api.has_permission(access_level='user'),)
    schema = PersonSchema
    data_layer = {'session': db.session, 'model': Person}
