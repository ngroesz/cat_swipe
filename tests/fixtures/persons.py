import pytest
import simplejson as json

from os.path import dirname, join, realpath
from web_service.models.person import Person

@pytest.fixture(scope='function')
def create_persons(_db):
    with open(join(dirname(realpath(__file__)), 'fixture_data', 'persons.json'), 'r') as f:
        persons = json.load(f)
        for person in persons:
            new_person = Person(name=person['name'])

            optional_parameters = ['age']
            for parameter in optional_parameters:
                if parameter in person:
                    setattr(new_person, parameter, person[parameter])

            _db.add(new_person)

    _db.commit()
