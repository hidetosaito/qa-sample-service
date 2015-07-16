#
# refer to http://boto3.readthedocs.org/en/latest/guide/sqs.html
#

import boto3
import json
import logging


class Queue(object):

    def __init__(self, region_name, queue_name, logger=logging.getLogger(__name__)):
        sqs = boto3.resource('sqs', region_name=region_name)
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)
        self.logger = logger

    def push(self, data):
        self.queue.send_message(MessageBody=json.dumps(data))

    def pop(self):
        return self.queue.receive_messages()