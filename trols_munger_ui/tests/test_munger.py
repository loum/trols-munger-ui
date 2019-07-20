"""Munger test cases.
"""
import urllib


def test_munger_singles_club_stats(test_client):
    """Test munger singles club stats.
    """
    # Given a query string
    query_kwargs = {
        'event': 'singles',
        'team': 'Watsonia',
    }
    query_string = urllib.parse.urlencode(query_kwargs)

    # when I source the default NETJA Saturday Spring 2015 stats
    response = test_client.get('/munger?{}'.format(query_string))

    # then I should get a 200 response
    msg = 'Singles club based stats response code error'
    assert response.status_code == 200, msg


def test_munger_doubles_club_stats(test_client):
    """Test munger doubles club stats.
    """
    # Given a query string
    query_kwargs = {
        'event': 'doubles',
        'team': 'Watsonia',
    }
    query_string = urllib.parse.urlencode(query_kwargs)

    # when I source the default NETJA Saturday Spring 2015 stats
    response = test_client.get('/munger?{}'.format(query_string))

    # then I should get a 200 response
    msg = 'Doubles club based stats response code error'
    assert response.status_code == 200, msg
