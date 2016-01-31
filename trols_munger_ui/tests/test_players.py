import unittest2
import urllib
import os
import json

import trols_munger_ui


class TestPlayers(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

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
            'q': 'Watsonia Blue'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the players URL
        response = self.__app.get('/munger/players?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players check response code'
        self.assertEqual(received, expected, msg)

    def test_players_json(self):
        """Test the player search URL.
        """
        # Given a query string
        kwargs = {
            'q': 'Markovski',
            'json': 'true'
        }
        query = urllib.urlencode(kwargs)

        # when I send to the search URL
        response = self.__app.get('/munger/players?{}'.format(query))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Players search check response code'
        self.assertEqual(received, expected, msg)

        # and I should get a JSON structure
        received = json.loads(response.data)
        with open(os.path.join(self.__results_dir,
                               'player_query_response.json')) as _fh:
            expected = json.loads(_fh.read().rstrip())
        msg = 'Player search JSON response error'
        self.assertEqual(received, expected, msg)

    def test_players_json_lowercase(self):
        """Test the player search URL: lowercase.
        """
        query_kwargs = {
            'q': 'joel markovski',
            'json': 'true'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the search URL
        response = self.__app.get('/munger/players?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Search check response code'
        self.assertEqual(received, expected, msg)

        # and I should get a JSON structure
        received = json.loads(response.data)
        with open(os.path.join(self.__results_dir,
                               'lc_player_query_response.json')) as _fh:
            expected = json.loads(_fh.read().rstrip())
        msg = 'Player search JSON response error (lowercase)'
        self.assertDictEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
