import simplejson as json


def to_array(rows):
    result = [row.as_dict() for row in rows]
    return json.dumps(result)
