import unittest2
import os
import tempfile
import json
import urllib

import trols_munger_ui
from filer.files import (remove_files,
                         get_directory_files_list,
                         move_file)


class TestSections(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__app =  trols_munger_ui.app.test_client()

    def test_sections(self):
        """Test sections call.
        """
        # When I source the default NETJA Saturday Spring 2015 teams
        response = self.__app.get('/_sections')

        # then I should get a 200 response
        msg = 'Sections list (_sections) response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the JSON teams list should match
        received = json.loads(response.data)
        expected = range(1, 27)
        msg = 'Sections list mis-match'
        self.assertEqual(received.get('sections'), expected, msg)

    def test_teams_competition_type_girls(self):
        """Sections teams call: competition type "girls".
        """
        # When I source the default NETJA Saturday Spring 2015
        # girls sections
        query = {
            'competition': 'nejta_saturday_am_spring_2015',
            'type': 'girls'
        }
        query_params = urllib.urlencode(query)
        response = self.__app.get('/_sections?{}'.format(query_params))

        # then I should get a 200 response
        msg = 'Sections list for comp_type response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the JSON sections list should match
        received = json.loads(response.data)
        expected = range(1, 15)
        msg = 'Sections for comp_type "girls" list mis-match'
        self.assertEqual(received.get('sections'), expected, msg)
