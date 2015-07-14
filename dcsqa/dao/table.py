'''
Created on Jul 9, 2015

@author: Hideto Saito
'''

import boto3
from flask import current_app
from boto3.dynamodb.conditions import Key, Attr

#
# refer to https://boto3.readthedocs.org/en/latest/guide/dynamodb.html
#


class DataTable(object):

    def __init__(self, region_name, table_name):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def find_all(self):
        #full scan
        response = self.table.scan()
        if response['Count'] > 0:
            return response['Items']
        else:
            current_app.logger.warn("there are no record in %s" % self.table.name)
            return None        

    def find_by_ticketkey(self, ticket_key):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key)
        )
        if response['Count'] > 0:
            return response['Items']
        else:
            current_app.logger.warn("there are no record TicketKey=%s in %s" % (ticket_key, self.table.name))
            return None

    def find_by_ticketkey_host(self, ticket_key, host):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Host').eq(host)
        )
        
        if response['Count'] > 0:
            items = response['Items']
            #not return array
            return items[0]
        else:
            current_app.logger.warn("there are no record TicketKey=%s, Host=%s in %s" % (ticket_key, host, self.table.name))
            return None
        
    def save(self, monitor_criteria_json):
        response = self.table.put_item(Item=monitor_criteria_json)
        current_app.logger.info(response)
        return response
    
    def update(self, ticket_key, monitor_criteria_json):
        pass
    
    def delete(self, ticket_key):
        pass