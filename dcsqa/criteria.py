#!/bin/env python
# coding: utf-8

import decimal
import json

from flask import request, make_response
from flask.ext.api import status
from flask import Blueprint
from dcsqa.dao.table import DataTable
from flask import current_app

criteria_blueprint = Blueprint('criteria', __name__)

# TODO - move out as utils
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


@criteria_blueprint.route('/', methods=['GET'])
def get_all_criteria():
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['CRITERIA_TABLE'])
    result = criteria.find_all()
    return _get_response_json(result)


@criteria_blueprint.route('/<ticket_key>', methods=['GET'])
def get_criteria_by_ticketkey(ticket_key):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['CRITERIA_TABLE'])
    result = criteria.find_by_ticketkey(ticket_key)
    return _get_response_json(result)


@criteria_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
def get_criteria_by_ticketkey_host(ticket_key, host):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['CRITERIA_TABLE'])
    result = criteria.find_by_ticketkey_host(ticket_key, host)
    return _get_response_json(result)


@criteria_blueprint.route('/', methods=['POST'])
def set_criteria_by_ticketkey_host():
    
    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. JSON must has TicketKey
    #    4. JSON must has Host
    #    5. enqueue
    #
    
    # 1.
    if request.headers['Content-Type'] != 'application/json':
        return make_response('please send application/json', status.HTTP_400_BAD_REQUEST)
    
    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception as ex:
        #criteria_blueprint.loo
        return make_response('invalid JSON format', status.HTTP_400_BAD_REQUEST)
    
    # 3.
    if 'TicketKey' not in data:
        return make_response('TiketKey is not found', status.HTTP_400_BAD_REQUEST)
    
    # 4.
    if 'Host' not in data:
        return make_response('Host is not found', status.HTTP_400_BAD_REQUEST)
    
    dao = DataTable(region_name=current_app.config['DYNAMODB_REGION'], table_name=current_app.config['CRITERIA_TABLE'])
    result = dao.save(data)

    return make_response('ok', status.HTTP_201_CREATED)

