import unittest
import os
import urllib

import trols_munger_ui


class TestMunger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shelve_dir = os.path.join('trols_munger_ui', 'tests', 'files')
        trols_munger_ui.app.config['SHELVE'] = shelve_dir
        cls.__app = trols_munger_ui.app.test_client()

    def test_munger_singles_club_stats(self):
        """Test munger singles club stats.
        """
        # Given a query string
        query_kwargs = {
            'event': 'singles',
            'team': 'Watsonia',
        }
        query_string = urllib.parse.urlencode(query_kwargs)

        # when I source the default NETJA Saturday Spring 2015 stats
        response = self.__app.get('/munger?{}'.format(query_string))

        # then I should get a 200 response
        msg = 'Singles club based stats response code error'
        self.assertEqual(response.status_code, 200, msg)

    def test_munger_doubles_club_stats(self):
        """Test munger doubles club stats.
        """
        # Given a query string
        query_kwargs = {
            'event': 'doubles',
            'team': 'Watsonia',
        }
        query_string = urllib.parse.urlencode(query_kwargs)

        # when I source the default NETJA Saturday Spring 2015 stats
        response = self.__app.get('/munger?{}'.format(query_string))

        # then I should get a 200 response
        msg = 'Doubles club based stats response code error'
        self.assertEqual(response.status_code, 200, msg)
