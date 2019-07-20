"""health route unit test cases.

"""
def test_health(test_client):
    """Test the health URL.
    """
    response = test_client.get('/munger/health')
    msg = 'Health check response code'
    assert response.status_code == 200, msg
