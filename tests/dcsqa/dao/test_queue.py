import unittest
import mock
import json
from mock import Mock
from dcsqa.dao.queue import Queue

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
            return self._message_queue.pop()
        else:
            return None

class TestingQueue(Queue):

    def __init__(self, region_name, queue_name):
        self.queue = MockSQS()


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
        self.assertEqual(json.dumps('test!'), item)
