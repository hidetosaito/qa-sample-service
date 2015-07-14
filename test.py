'''
Created on Jul 11, 2015

@author: Hideto Saito
'''
import server
import unittest
from mock import Mock

class UnitTestCase(unittest.TestCase):


    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def testRoot(self):
        rv = self.app.get('/')
        self.assertEqual('please use API', rv.data)

    def test_get_all_criteria(self):
        # moto doesn't work well with boo3, should use mock to perform unit test
        #rv = self.app.get('/criteria')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()