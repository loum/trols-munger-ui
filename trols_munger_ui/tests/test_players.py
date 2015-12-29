import unittest2
import urllib
import os

import trols_munger_ui


class TestPlayers(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        shelve_dir = os.path.join('trols_munger_ui', 'tests', 'files')
        trols_munger_ui.app.config['SHELVE'] = shelve_dir
        cls.__app = trols_munger_ui.app.test_client()

        cls.__results_dir = os.path.join('trols_munger_ui',
                                         'tests',
                                         'results')

    def test_players(self):
        """Test the players URL.
        """
        # Given a query string
        query_kwargs = {
            'q': 'Isabella Markovski'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the players URL
        response = self.__app.get('/munger/players?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players check response code'
        self.assertEqual(received, expected, msg)

    def test_players_team_search(self):
        """Test the players URL: team search.
        """
        # Given a team query string
        query_kwargs = {
            'q': 'Watsonia'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the players URL
        response = self.__app.get('/munger/players?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players check response code'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
