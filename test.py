'''
Created on Jul 11, 2015

@author: Hideto Saito
'''
from dcsqa.app import app
import unittest
from mock import Mock


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def testRoot(self):
        rv = self.app.get('/')
        self.assertEqual('please use API', rv.data)

    def test_get_all_criteria(self):
        # moto doesn't work well with boto3, should use mock to perform unit test
        #rv = self.app.get('/criteria')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()