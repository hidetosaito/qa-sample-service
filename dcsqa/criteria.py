#!/bin/env python
# coding: utf-8

import response
from dcsqa.dao.table import DataTable
from dcsqa.dao.queue import Queue
from auth import auth
from flask import request, Blueprint, current_app

criteria_blueprint = Blueprint('criteria', __name__)

@criteria_blueprint.before_request
@auth.login_required
def before_request():
    current_app.logger.debug("user login - {user}".format(user=auth.username()))


@criteria_blueprint.route('', methods=['GET'])
def get_all_criteria():
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = current_app.cache.get('criteria.all')
    if result is None:
        result = criteria.find_all()
        current_app.cache.set('criteria.all', result)
        
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>', methods=['GET'])
def get_criteria_by_ticketkey(ticket_key):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = current_app.cache.get("criteria.ticket_key.%s" % ticket_key)
    if result is None:
        result = criteria.find_by_ticketkey(ticket_key)
        current_app.cache.set("criteria.ticket_key.%s" % ticket_key, result)
        
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
def get_criteria_by_ticketkey_host(ticket_key, host):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = current_app.cache.get("criteria.ticket_key.%s.host.%s" % (ticket_key, host))
    if result is None:
        result = criteria.find_by_ticketkey_host(ticket_key, host)
        current_app.cache.set("criteria.ticket_key.%s.host.%s" % (ticket_key, host), result)
    return response.get_json(result)


@criteria_blueprint.route('', methods=['POST'])
def set_criteria_by_ticketkey_host():
    
    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. JSON must has TicketKey and Host
    #    4. save to DB
    #    5. purge cache
    #    6. enqueue
    #
    
    # 1.
    if request.headers['Content-Type'] != 'application/json':
        current_app.logger.warn("received Content-Type %s" % request.headers['Content-Type'])
        return response.bad_request("please send application/json")

    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception as ex:
        current_app.logger.warn("couldn't parse JSON %s" % ex)
        return response.bad_request("invalid JSON format")

    # 3.
    required_key = ['TicketKey', 'Host']
    for key in required_key:
        if key not in data:
            return response.bad_request("{key} is not found".format(key=key))

    # 4.
    table = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['CRITERIA_TABLE'],
                    logger=current_app.logger)
    result = table.save(data)

    # 5.
    current_app.cache.delete('criteria.all')
    current_app.cache.delete("criteria.ticket_key.%s" % data['TicketKey'])
    current_app.cache.delete("criteria.ticket_key.%s.host.%s" % (data['TicketKey'], data['Host']))
 

    # 6.
    queue = Queue(region_name=current_app.config['SQS_REGIOM'],
                  queue_name=current_app.config['SQS_NAME'],
                  logger=current_app.logger)
    queue.push({key: data[key] for key in required_key})

    return response.created()

