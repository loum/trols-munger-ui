import unittest2

import trols_munger_ui


class TestHealth(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        trols_munger_ui.app.config['SHELVE'] = '/var/tmp/trols_shelve'
        cls.__app =  trols_munger_ui.app.test_client()

    def test_health(self):
        """Test the health URL.
        """
        response = self.__app.get('/munger/health')
        msg = 'Health check response code'
        self.assertEqual(response.status_code, 200, msg)
