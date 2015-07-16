import unittest
import base64
import boto3
import json
import mock
from entry import app
from moto.dynamodb2 import mock_dynamodb2
from moto.sqs import mock_sqs
from dcsqa.dao.queue import Queue

class CriteriaRequestTest(unittest.TestCase):

    def setUp(self):
        self.region_name = 'us-east-1'
        self.table_name = 'test-Criteria'
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()

    def _create_table(self):
        dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'TicketKey',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Host',
                    'AttributeType': 'S'
                },
                ],
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'TicketKey',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Host',
                    'KeyType': 'RANGE'
                },
                ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )

    def _get_auth_header(self, json=False):
        header = {'Authorization': 'Basic ' + base64.b64encode("{0}:{1}".format('dcsrd', 'happy'))}
        if json:
            header['Content-Type'] = 'application/json'
        return header

    @mock_dynamodb2
    @mock.patch('dcsqa.criteria.Queue')
    def test_post_criteria(self, mock_queue):
        self._create_table()

        # test no content
        self.assertEqual(204, self.app.get('/criteria', headers=self._get_auth_header()).status_code)

        # test post 400 wrong header
        response = self.app.post('/criteria', headers=self._get_auth_header(),
                                 data=dict(TickeKey='testKey', Host='test'),
                                 follow_redirects=True)
        self.assertEqual(400, response.status_code)
        self.assertEqual("please send application/json", response.data)

        # test post 400 wrong key
        response = self.app.post('/criteria', headers=self._get_auth_header(json=True),
                                 data=json.dumps(dict(TicketKey='testKey')), follow_redirects=True)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Host is not found", response.data)

        # test success
        response = self.app.post('/criteria', headers=self._get_auth_header(json=True),
                                 data=json.dumps(dict(TicketKey='testKey', Host='test')),
                                 follow_redirects=True)
        self.assertEqual(201, response.status_code)

