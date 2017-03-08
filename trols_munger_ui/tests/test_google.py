import unittest

import trols_munger_ui


class TestGoogle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__app =  trols_munger_ui.app.test_client()

    def test_robots(self):
        """Test robots.txt
        """
        response = self.__app.get('/robots.txt')
        msg = 'robots.txt check response code'
        self.assertEqual(response.status_code, 200, msg)

    def test_sitemap(self):
        """Test sitemap.
        """
        response = self.__app.get('/sitemap.xml')
        msg = 'sitemap.xml check response code'
        self.assertEqual(response.status_code, 200, msg)
