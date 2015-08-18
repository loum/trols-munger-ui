import unittest2
import urllib
import os

import trols_munger_ui


class TestSearch(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        shelve_dir = os.path.join('trols_munger_ui', 'tests', 'files')
        trols_munger_ui.app.config['SHELVE'] = shelve_dir
        cls.__app = trols_munger_ui.app.test_client()

        cls.__results_dir = os.path.join('trols_munger_ui',
                                         'tests',
                                         'results')

    def test_search(self):
        """Test the search URL.
        """
        # Given a query string
        kwargs = {
            'q': 'Isabella Markovski'
        }
        query = urllib.urlencode(kwargs)

        # when I send to the search URL
        response = self.__app.get('/munger/search?{}'.format(query))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Search check response code'
        self.assertEqual(received, expected, msg)

        # and I should get a JSON structure
        received = response.data
        with open(os.path.join(self.__results_dir,
                               'player_query_response.json')) as _fh:
            expected = _fh.read().rstrip()
        msg = 'Player search JSON response error'
        self.assertEqual(received, expected, msg)

    def test_search_part_name_lowercase(self):
        """Test the search URL: part name lowercase.
        """
        # Given a query string
        query_kwargs = {
            'q': 'markovski'
        }
        query_string = urllib.urlencode(query_kwargs)

        # when I send to the search URL
        response = self.__app.get('/munger/search?{}'.format(query_string))

        # then I should get ...
        received = response.status_code
        expected = 200
        msg = 'Search check response code'
        self.assertEqual(received, expected, msg)

        # and I should get a JSON structure
        received = response.data
        with open(os.path.join(self.__results_dir,
                               'part_player_query_response.json')) as _fh:
            expected = _fh.read().rstrip()
        msg = 'Player search JSON response error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls.__results_dir
