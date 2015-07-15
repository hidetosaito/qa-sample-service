#!/bin/env python
# coding: utf-8

import response
from dcsqa.dao.table import DataTable
from dcsqa.dao.queue import Queue
from flask import request
from flask import Blueprint
from flask import current_app

criteria_blueprint = Blueprint('criteria', __name__)


@criteria_blueprint.route('', methods=['GET'])
def get_all_criteria():
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_all()
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>', methods=['GET'])
def get_criteria_by_ticketkey(ticket_key):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_by_ticketkey(ticket_key)
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
def get_criteria_by_ticketkey_host(ticket_key, host):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_by_ticketkey_host(ticket_key, host)
    return response.get_json(result)


@criteria_blueprint.route('', methods=['POST'])
def set_criteria_by_ticketkey_host():
    
    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. JSON must has TicketKey
    #    4. JSON must has Host
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
    if 'TicketKey' not in data:
        return response.bad_request("TiketKey is not found")

    # 4.
    if 'Host' not in data:
        return response.bad_request("Host is not found")

    dao = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['CRITERIA_TABLE'],
                    logger=current_app.logger)
    result = dao.save(data)

    # 5.
    queue = Queue(region_name=current_app.config['SQS_REGIOM'],
                  queue_name=current_app.config['SQS_NAME'],
                  logger=current_app.logger)
    queue.push(data)

    return response.is_okay()

