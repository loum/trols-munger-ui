import unittest2
import urllib
import os

import trols_munger_ui


class TestStats(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        shelve_dir = os.path.join('trols_munger_ui', 'tests', 'files')
        trols_munger_ui.app.config['SHELVE'] = shelve_dir
        cls.__app = trols_munger_ui.app.test_client()

        cls.__results_dir = os.path.join('trols_munger_ui',
                                         'tests',
                                         'results')

    def test_stats(self):
        """Test the stats URL.
        """
        # Given a query token
        query_kwargs = {
            'token':
                'Isabella Markovski|Watsonia Blue|14|girls|saturday_am_autumn_2015'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the players URL
        response = self.__app.get('/munger/stats?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players check response code'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
