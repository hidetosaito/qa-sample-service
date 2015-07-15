import unittest
import base64
from entry import app

class AuthosrizedTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def _request(self, username, password):
        headers = {'Authorization': 'Basic ' + base64.b64encode("{0}:{1}".format(username, password))}
        return self.app.get('/login', headers=headers)

    def test_login_unauthorized(self):
        rv = self._request('admin', 'default')
        self.assertEqual(401, rv.status_code)

    def test_login_success(self):
        rv = self._request('dcsrd', 'happy')
        self.assertEqual(200, rv.status_code)


