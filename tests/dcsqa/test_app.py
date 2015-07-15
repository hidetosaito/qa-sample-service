'''
Created on Jul 11, 2015

@author: Hideto Saito
'''
from dcsqa.app import app
import unittest


class RootAppTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual('please use API', rv.data)

