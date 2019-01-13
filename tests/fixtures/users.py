import pytest
import simplejson as json

from os.path import dirname, join, realpath
from web_service.models.user import User

@pytest.fixture(scope='function')
def create_users(_db):
    with open(join(dirname(realpath(__file__)), 'fixture_data', 'users.json'), 'r') as f:
        users = json.load(f)
        for user in users:
            new_user = User(username=user['username'], password=user['password'])

            optional_parameters = ['email', 'is_admin']
            for parameter in optional_parameters:
                if parameter in user:
                    setattr(new_user, parameter, user[parameter])

            _db.add(new_user)

    _db.commit()
