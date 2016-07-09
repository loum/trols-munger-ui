import unittest2
import os
import tempfile
import json
import urllib

import trols_munger_ui
from filer.files import (remove_files,
                         get_directory_files_list,
                         move_file)


class TestTeams(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__app =  trols_munger_ui.app.test_client()

    def test_teams(self):
        """Test teams call.
        """
        # When I source the default NEJTA Saturday Spring 2015 teams
        response = self.__app.get('/_teams')

        # then I should get a 200 response
        msg = 'Teams list (_teams) response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the JSON teams list should match
        result = json.loads(response.data)
        received = sorted(result.get('teams'))
        expected = 'Watsonia'
        msg = 'Teams list mis-match'
        self.assertEqual(received[67], expected, msg)

    def test_teams_competition_type(self):
        """Test teams call: competition type.
        """
        # When I source the default NETJA Saturday Spring 2015 teams
        query = {
            'competition': 'nejta_saturday_am_spring_2015',
            'type': 'girls'
        }
        query_params = urllib.urlencode(query)
        response = self.__app.get('/_teams?{}'.format(query_params))

        # then I should get a 200 response
        msg = 'Teams list for comp_type response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the JSON teams list should match
        received = json.loads(response.data)
        expected = u'Watsonia'
        msg = 'Teams for comp_type list mis-match'
        self.assertEqual(received.get('teams')[40], expected, msg)

    def test_teams_competition_type_and_section(self):
        """Test teams call: competition type and section.
        """
        # When I source the default NETJA Saturday Spring 2015 teams
        query = {
            'competition': 'nejta_saturday_am_spring_2015',
            'type': 'boys',
            'section': '21'
        }
        query_params = urllib.urlencode(query)
        response = self.__app.get('/_teams?{}'.format(query_params))

        # then I should get a 200 response
        msg = 'Teams list for comp_type and section response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the JSON teams list should match
        received = json.loads(response.data)
        expected = u'Watsonia'
        msg = 'Teams list for comp_type and section mis-match'
        self.assertEqual(received.get('teams')[7], expected, msg)

    def test_teams_no_matches(self):
        """Test teams call: no matches.
        """
        # When I source the default NEJTA Saturday Spring 2015 teams
        response = self.__app.get('/_teams/nejta_saturday_am_spring_2015/girls/21')
        query = {
            'competition': 'nejta_saturday_am_spring_2015',
            'type': 'girls',
            'section': '21'
        }
        query_params = urllib.urlencode(query)
        response = self.__app.get('/_teams?{}'.format(query_params))

        # then I should get a 200 response
        msg = 'Teams list for comp_type and section response code'
        self.assertEqual(response.status_code, 200, msg)

        # and an empty JSON teams list
        received = json.loads(response.data)
        expected = []
        msg = 'Teams list should be empty'
        self.assertListEqual(received.get('teams'), expected, msg)
