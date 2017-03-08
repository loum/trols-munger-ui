"""Unit tests for the Stats view.

"""
import unittest
import urllib
import os
import json

import trols_munger_ui


class TestStats(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

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
                'Isabella Markovski~Watsonia Blue~14~girls~'
                'nejta_saturday_am_autumn_2015',
            'json': 'true',
        }
        query_string = urllib.parse.urlencode(query_kwargs)

        # when I send to the players URL
        response = self.__app.get('/munger/stats?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players check response code'
        self.assertEqual(received, expected, msg)

        # and I should get a JSON structure
        received = json.loads(response.data.decode('utf-8'))
        with open(os.path.join(self.__results_dir,
                               'one_player_stats.json')) as _fh:
            expected = json.loads(_fh.read().rstrip())
        msg = 'Player stats JSON response error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
