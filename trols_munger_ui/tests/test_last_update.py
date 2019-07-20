import os

import trols_munger_ui


def test_last_update(test_client):
    """Test the last update UTC timestamp.
    """
    # Given a shelve DB file

    # and a known timestamp
    os.utime(trols_munger_ui.app.config['SHELVE_DB'], (1440901349, 1440901349))

    # when I source the shelve's modfied time stamp
    response = test_client.get('/_last_update')

    # then I should get a 200 response
    msg = 'Health _last_update response code'
    assert response.status_code == 200, msg

    # and the UTC time should match
    received = response.data
    expected = '{"last_update":"2015-08-30T02:22:29Z"}'
    msg = 'Last updated UTC time mis-match'
    assert received.rstrip().decode('utf-8') == expected, msg
