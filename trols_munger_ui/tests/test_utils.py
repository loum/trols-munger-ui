import unittest2
import urllib

from trols_munger_ui.utils import query_terms_to_dict


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
        terms = {'q': ['joel', 'eboni']}
        request = '{}?{}'.format(self.__base_url,
                                 urllib.urlencode(terms, doseq=True))

        received = query_terms_to_dict(request)
        expected = {'q': ['joel', 'eboni']}
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
