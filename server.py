#!/bin/env python
# coding: utf-8

import os
import decimal
import json

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, request, make_response

DYNAMODB_REGION = 'us-west-1'
DYNAMODB_TABLE = 'QAPortal-Staging-Criteria'

app = Flask(__name__)
app.debug = True

# http://flask.pocoo.org/docs/0.10/tutorial/setup/
app.config.from_object(__name__)
dynamodb = boto3.resource('dynamodb', region_name=app.config['DYNAMODB_REGION'])


def _convert_decimal_to_int(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)

def _get_response_json(obj):
    if obj != None:
        response = make_response(json.dumps(obj, default=_convert_decimal_to_int))
    else:
        response = make_response('', 204) #HTTP 204(NO CONTENT) when no result
    
    response.mimetype='application/json'
    
    return response


@app.route('/')
def index():
    return 'please use API'


@app.route('/criteria', methods=['GET'])
def get_all_criteria():
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])   
      
    response = table.scan() #full scan
    if response['Count'] > 0:
        return _get_response_json(response['Items'])
    else:
        app.logger.warn("there are no record in %s" % app.config['DYNAMODB_TABLE'])
        return _get_response_json(None)


@app.route('/criteria/<ticket_key>', methods=['GET'])
def get_criteria_by_ticketkey(ticket_key):
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])     

    response = table.query(
        KeyConditionExpression=Key('TicketKey').eq(ticket_key)
    )
    
    if response['Count'] > 0:
        return _get_response_json(response['Items'])
    else:
        app.logger.warn("there are no record TicketKey=%s in %s" % (ticket_key, app.config['DYNAMODB_TABLE']))
        return _get_response_json(None)


@app.route('/criteria/<ticket_key>/<host>', methods=['GET'])
def get_criteria_by_ticketkey_host(ticket_key, host):
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])     

    response = table.query(
        KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Host').eq(host)
    )
        
    if response['Count'] > 0:
        items = response['Items']
        return _get_response_json(items[0]) #not return array
    else:
        app.logger.warn("there are no record TicketKey=%s, Host=%s in %s" % (ticket_key, host, app.config['DYNAMODB_TABLE']))
        return _get_response_json(None)


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
        app.logger.warn("received Content-Type %s" % request.headers['Content-Type'])
        return make_response('please send application/json', 400)
    
    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception, e:
        app.logger.warn("couldn't parse JSON %s" % e)
        return make_response('invalid JSON format', 400)
    
    # 3.
    if 'TicketKey' not in data:
        return make_response('TiketKey is not found', 400)
    
    # 4.
    if 'Host' not in data:
        return make_response('Host is not found', 400)
    
    #store to table
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])     
    response = table.put_item(Item=data)
    app.logger.info(response)

    return make_response('ok', 201)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
