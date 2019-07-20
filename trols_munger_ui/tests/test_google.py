"""`trols_munger_ui Google view unit test cases.

"""
def test_robots(test_client):
    """Test robots.txt
    """
    response = test_client.get('/robots.txt')
    msg = 'robots.txt check response code'
    assert response.status_code == 200, msg


def test_sitemap(test_client):
    """Test sitemap.
    """
    response = test_client.get('/sitemap.xml')
    msg = 'sitemap.xml check response code'
    assert response.status_code == 200, msg
