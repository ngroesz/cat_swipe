"""
The __init__.py file sets up routes for the API
Each API module also defines a schema.
The relevant modules are flask-rest-jsonapi and marshmallow-jsonapi
To see a list of route endpoints and URLs, do something like:
> flask routes
"""

from web_service.api.bootstrap import api

from web_service.api.cat_api import CatDetailApi, CatListApi
from web_service.api.person_api import PersonDetailApi, PersonListApi
from web_service.api.swipe_api import SwipeDetailApi, SwipeListApi

api.route(CatDetailApi, 'cat_detail', '/cat')
api.route(CatListApi, 'cat_list', '/cats')

api.route(PersonDetailApi, 'person_detail', '/person')
api.route(PersonListApi, 'person_list', '/persons')

api.route(SwipeDetailApi, 'swipe_detail', '/swipe')
api.route(SwipeListApi, 'swipe_list', '/swipes')
