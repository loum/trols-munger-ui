"""General utils.

"""
import urllib.parse
import logging


def query_terms_to_dict(request, key_preamble=None):
    """Parse and extract raw query string from *request*

    **Args:**
        *request*: the URL request string.  For example::

            http://www.example.com/myapplication/page.html?x=y

        *key_preamble*: override the search key taken from the URL
        query terms parse by prepending the *key_preamble* token to
        the resultant dictionary structure.  For example, if the
        *key_preamble* is ``metadata=``::

            {'NITF_IREP': ['MONO']}

        becomes::

             {'metadata=NITF_IREP': ['MONO']}

    **Returns:**
        dictionary structure as per :func:`urllib.parse.parse_qs` where the
        keys are unique query variable names and the values are lists of
        values for each name

    """
    logging.debug('Parsing query terms request: %s', request)

    logging.debug('Unquoted: %s', urllib.parse.unquote(request))

    parser = urllib.parse.urlparse(request)
    query_strings = urllib.parse.parse_qs(parser.query)

    if key_preamble is not None:
        tmp_query_strings = dict(query_strings)
        query_strings.clear()
        for key, value in tmp_query_strings.items():
            query_strings['%s%s' % (key_preamble, key)] = value

    logging.debug('Parsed query strings: %s', query_strings)

    return query_strings
