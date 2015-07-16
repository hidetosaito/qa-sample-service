import unittest
import boto3
from moto.dynamodb2 import mock_dynamodb2
from dcsqa.dao.table import DataTable

class DataTableTest(unittest.TestCase):

    def setUp(self):
        self.table_name = 'test'
        self.region_name = 'us-east-1'
        self.hash_key = 'hashkey'
        self.range_key = 'rangekey'

    def _create_table(self):
        dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        response = dynamodb.create_table(
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

    def _stuff_test_items(self, table, hashkey='test', item_cnt=1):
        for i in range(item_cnt):
            test_item = {
                'Host': 'test-host-{idx}'.format(idx=i),
                'TicketKey': hashkey
            }
            table.save(test_item)

    @mock_dynamodb2
    def test_find_all(self):
        self._create_table()
        table = DataTable(region_name=self.region_name, table_name=self.table_name)
        self.assertIsNone(table.find_all())

        self._stuff_test_items(table)
        self.assertIsNotNone(table.find_all())
        self.assertEqual(1, len(table.find_all()))

    @mock_dynamodb2
    def test_save(self):
        self._create_table()
        table = DataTable(region_name=self.region_name, table_name=self.table_name)
        self.assertIsNone(table.find_all())

        self._stuff_test_items(table, item_cnt=3)
        self.assertEqual(3, len(table.find_all()))


