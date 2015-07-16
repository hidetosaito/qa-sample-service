import unittest
import mock
import json
import logging
from mock import Mock
from dcsqa.dao.queue import Queue

class MockMessage(object):

    def __init__(self, message):
        self.message = message
        self.queue_url = 'https://queue.amazonaws.com/'
        self.receipt_handle = 'ABCDE'

    def __str__(self):
        return "queue_url={queue_url}, receipt_handle={receipt_handle}".\
            format(queue_url=self.queue_url, receipt_handle=self.receipt_handle)

    @property
    def body(self):
        return self.message


class MockSQS(object):

    _message_queue = []

    def send_message(self, MessageBody):
        self._message_queue.append(MessageBody)
        return {
            'MessageId': 'test123',
            'MD5OfMessageBody': MessageBody
        }

    def receive_messages(self):
        if len(self._message_queue) > 0:
            message =  self._message_queue.pop()
            return [MockMessage(message)]
        else:
            return None

class TestingQueue(Queue):

    def __init__(self, region_name, queue_name, logger=logging.getLogger(__name__)):
        self.queue = MockSQS()
        self.logger = logger


class QueueTest(unittest.TestCase):

    def setUp(self):
        self.queue_name = 'test'
        self.region_name = 'us-east-1'

    """
    # moto didn't support 'send_message' action
    def _create_queue(self):
        sqs = boto3.resource('sqs', region_name=self.region_name)
        sqs.create_queue(QueueName=self.queue_name)
        #self.queue = sqs.get_queue_by_name(QueueName=self.queue_name)
    """

    def test_push(self):

        queue = TestingQueue(region_name=self.region_name, queue_name=self.queue_name)
        queue.push('test!')
        item = queue.pop()
        self.assertIsNotNone(item)
        self.assertEqual('test!', item)

        message = {'test': 'yes', 'happy': 'maybe'}
        queue.push(json.dumps(message))
        item = queue.pop()
        self.assertEqual(json.dumps(message), item)

