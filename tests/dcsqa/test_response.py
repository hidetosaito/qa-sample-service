import unittest
from dcsqa.app import app
import dcsqa.response as response
from decimal import Decimal

class ResponseTest(unittest.TestCase):

    def setUp(self):
        #
        # to resolve 'working outside of application context' error when make_reponse
        # refer to http://flask.pocoo.org/docs/0.10/appcontext/
        #
        app.config.from_object('config.TestConfig')
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_json(self):
        test_response = [{u'Hostname': u'dcs-qauat01.sjdc', u'Memory': Decimal('0'),
                          u'OSType': u'linux', u'CPU': Decimal('0'),
                          u'DataPartition': [{u'name': u'/', u'size': Decimal('20000')},
                                             {u'type': u'SAS', u'local': True,
                                              u'name': u'/trend', u'size': Decimal('80000')}]
                         }]

        self.assertEqual(200, response.get_json(test_response).status_code)
        self.assertEqual(200, response.get_json("").status_code)
        self.assertEqual(204, response.get_json(None).status_code)

    def test_bad_request(self):
        self.assertEqual(400, response.bad_request("it's really bad").status_code)
        self.assertEqual("it's really bad", response.bad_request("it's really bad").data)

    def test_created(self):
        self.assertEqual(201, response.created().status_code)
        self.assertEqual("ok", response.created().data)
