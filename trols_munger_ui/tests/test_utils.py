import unittest2
import urllib

from trols_munger_ui.utils import (query_terms_to_dict,
                                   player_ids_dict)


class TestUtils(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__base_url = '/munger/search'
    
    def test_query_terms_to_dict_single(self):
        """Parse query term strings: single term.
        """
        terms = {'q': 'isabella'}
        request = '{}?{}'.format(self.__base_url, urllib.urlencode(terms))

        received = query_terms_to_dict(request)
        expected = {'q': ['isabella']}
        msg = 'Single query term to dict conversion error'
        self.assertDictEqual(received, expected, msg)
    
    def test_query_terms_to_dict_multiple(self):
        """Parse query term strings: multiple term.
        """
        terms = {'q': 'isabella',
                 'q': ['joel', 'eboni']}
        request = '{}?{}'.format(self.__base_url,
                                 urllib.urlencode(terms, doseq=True))

        received = query_terms_to_dict(request)
        expected = {'q': ['isabella'],
                    'q': ['joel', 'eboni']}
        msg = 'Multiple query term to dict conversion error'
        self.assertDictEqual(received, expected, msg)
    
    def test_query_terms_to_dict_quotes(self):
        """Parse query term strings: quotes.
        """
        terms = {'q': ['joel', 'Isabella Markovski']}
        request = '{}?{}'.format(self.__base_url,
                                 urllib.urlencode(terms, doseq=True))

        received = query_terms_to_dict(request)
        expected = {'q': ['joel', 'Isabella Markovski']}
        msg = 'Quoted query term to dict conversion error'
        self.assertDictEqual(received, expected, msg)
    
    def test_query_terms_to_dict_single_with_preable(self):
        """Parse query term strings: single term with preamble.
        """
        terms = {'q': 'Isabella'}
        request = '{}?{}'.format(self.__base_url, urllib.urlencode(terms))

        received = query_terms_to_dict(request, key_preamble='metadata=')
        expected = {'metadata=q': ['Isabella']}
        msg = 'Single query term to dict conversion error'
        self.assertDictEqual(received, expected, msg)

    def test_player_ids_dict(self):
        """Test player_ids_dict.
        """
        # Given a list of player IDs
        players = [
            "John Guanzon|Epping|3|boys|saturday_am_spring_2015",
            "Whitney Guan|Clifton|2|girls|saturday_am_spring_2015",
        ]

        # when I convert to a dictionary structure
        received = player_ids_dict(players)

        # then I should receive the correct list of dictionaries
        expected = [
            {
                'comp': 'saturday_am_spring_2015',
                'comp_type': 'boys',
                'name': 'John Guanzon',
                'section': '3',
                'team': 'Epping'
            },
            {
                'comp': 'saturday_am_spring_2015',
                'comp_type': 'girls',
                'name': 'Whitney Guan',
                'section': '2',
                'team': 'Clifton'
            }
        ]
        msg = 'Player IDs to dict conversion error'
        self.assertListEqual(received, expected, msg)
