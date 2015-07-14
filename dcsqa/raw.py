#!/bin/env python
# coding: utf-8

import decimal
import json

from flask import request, make_response
from flask.ext.api import status
from flask import Blueprint
from dcsqa.dao.table import DataTable
from flask import current_app

raw_blueprint = Blueprint('raw', __name__)


def _convert_decimal_to_int(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)


def _get_response_json(obj):
    if obj != None:
        response = make_response(json.dumps(obj, default=_convert_decimal_to_int))
    else:
        response = make_response('', status.HTTP_204_NO_CONTENT)

    response.mimetype = 'application/json'

    return response


@raw_blueprint.route('/', methods=['GET'])
def get_all_raw():
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['RAW_TABLE'])
    result = raw.find_all()
    return _get_response_json(result)


@raw_blueprint.route('/<ticket_key>', methods=['GET'])
def get_raw_by_ticketkey(ticket_key):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['RAW_TABLE'])
    result = raw.find_by_ticketkey(ticket_key)
    return _get_response_json(result)


@raw_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
def get_raw_by_ticketkey_host(ticket_key, host):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['RAW_TABLE'])
    result = raw.find_by_ticketkey_host(ticket_key, host)
    return _get_response_json(result)

