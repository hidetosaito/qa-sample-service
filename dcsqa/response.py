import json
import decimal
from flask import make_response
from flask.ext.api import status


def get_json(obj):
    def _convert_decimal_to_int(obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)

    if obj is not None:
        response = make_response(json.dumps(obj, default=_convert_decimal_to_int))
    else:
        response = make_response('', status.HTTP_204_NO_CONTENT)

    response.mimetype = 'application/json'

    return response


def bad_request(message):
    return make_response(message, status.HTTP_400_BAD_REQUEST)


def created():
    return make_response('ok', status.HTTP_201_CREATED)