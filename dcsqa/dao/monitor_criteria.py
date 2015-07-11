'''
Created on Jul 9, 2015

@author: Hideto Saito
'''

import boto3
from boto3.dynamodb.conditions import Key, Attr

#
# refer to https://boto3.readthedocs.org/en/latest/guide/dynamodb.html
#

class MonitorCriteria(object):

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        self.table = self.dynamodb.Table('QAPortal-Staging-Criteria') 

    
    def find_all(self):
        response = self.table.scan() #full scan
        if response['Count'] > 0:
            return response['Items']
        else:
            #log error
            return None        

    
    def find_by_ticketkey(self, ticket_key):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key)
        )
        if response['Count'] > 0:
            return response['Items']
        else:
            #log error
            return None


    def find_by_ticketkey_host(self, ticket_key, host):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Host').eq(host)
        )
        
        if response['Count'] > 0:
            items = response['Items']
            return items[0] #not return array
        else:
            #log error
            return None
        
    
    def save(self, monitor_criteria_json):
        response = self.table.put_item(Item=monitor_criteria_json)
        return response
    
    def update(self, ticket_key, monitor_criteria_json):
        pass
    
    def delete(self, ticket_key):
        pass