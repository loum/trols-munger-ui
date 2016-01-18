import urlparse
import urllib

from logga.log import log


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
        dictionary structure as per :func:`urlparse.parse_qs` where the
        keys are unique query variable names and the values are lists of
        values for each name

    """
    log.debug('Parsing query terms request: %s', request)

    log.debug('Unquoted: %s', urllib.unquote(request))

    parser = urlparse.urlparse(request)
    query_strings = urlparse.parse_qs(parser.query)

    if key_preamble is not None:
        tmp_query_strings = dict(query_strings)
        query_strings.clear()
        for key, value in tmp_query_strings.iteritems():
            query_strings['%s%s' % (key_preamble, key)] = value

    log.debug('Parsed query strings: %s', query_strings)

    return query_strings


def player_ids_dict(player_ids):
    """Helper method that splits the components of the token index
    from *player_ids* list into separate parts.  For example::

    >>> from trols_munder_ui.utils import player_ids_dict
    >>> token = ('Isabella Markovski~Watsonia~12~girls~'
    ...          'saturday_am_spring_2015')
    >>> player_ids_dict([token])
    [{'name': 'Isabella Markovski', 'comp_type': 'girls', 'section': '12',
    'team': 'Watsonia', 'token': 'Isabella Markovski~Watsonia~12~girls~sa
    turday_am_spring_2015', 'comp': 'saturday_am_spring_2015'}]

    """
    def player_id_struct(player_id):
        (name, team, section, comp_type, comp) = player_id.split('~')
        comp_parts = comp.split('_')
        comp_string = '{} {} {} {}'.format(comp_parts[0].title(),
                                           comp_parts[1].upper(),
                                           comp_parts[2].title(),
                                           comp_parts[3])

        return {
            'name': name,
            'team': team,
            'section': section,
            'comp_type': comp_type,
            'comp': comp,
            'comp_string': comp_string,
            'token': player_id,
        }

    return [player_id_struct(x) for x in player_ids]
