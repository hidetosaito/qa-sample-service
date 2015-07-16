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
        messages = self.queue.receive_messages()
        if len(messages):
            message = messages[0]
            try:
                return json.loads(message.body)
            except Exception as ex:
                self.logger.warn('cannot convert to json format')
                return message.body
        return None