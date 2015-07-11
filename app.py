#!/bin/env python
# coding: utf-8

import os
import decimal
import json

from flask import Flask, request, make_response
from dcsqa.dao.monitor_criteria import MonitorCriteria

app = Flask(__name__)
app.debug = True


def _convert_decimal_to_float(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)

def _get_response_json(obj):
    if obj != None:
        response = make_response(json.dumps(obj, default=_convert_decimal_to_float))
    else:
        response = make_response('', 204) #HTTP 204(NO CONTENT) when no result
    
    response.mimetype='application/json'
    
    return response


@app.route('/')
def index():
    return 'plese use API'


@app.route('/criteria', methods=['GET'])
def get_all_criteria():
    criteria = MonitorCriteria()
    result = criteria.find_all()
    return _get_response_json(result)


@app.route('/criteria/<ticket_key>', methods=['GET'])
def get_criteria_by_ticketkey(ticket_key):
    criteria = MonitorCriteria()
    result = criteria.find_by_ticketkey(ticket_key)
    return _get_response_json(result)


@app.route('/criteria/<ticket_key>/<host>', methods=['GET'])
def get_criteria_by_ticketkey_host(ticket_key, host):
    criteria = MonitorCriteria()
    result = criteria.find_by_ticketkey_host(ticket_key, host)
    return _get_response_json(result)


@app.route('/criteria', methods=['POST'])
def set_criteria_by_ticketkey_host():
    
    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. JSON must has TicketKey
    #    4. JSON must has Host
    #
    
    # 1.
    if request.headers['Content-Type'] != 'application/json' :
        return make_response('please send application/json', 400)
    
    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except:
        return make_response('invalid JSON format', 400)
    
    # 3.
    if 'TicketKey' not in data:
        return make_response('TiketKey is not found', 400)
    
    # 4.
    if 'Host' not in data:
        return make_response('Host is not found', 400)
    
    dao = MonitorCriteria()
    result = dao.save(data)

    return make_response('ok', 201)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
