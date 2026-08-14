import unittest
from app import app

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_landing_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PhishGuard AI", response.data)
        self.assertIn(b"Detect Phishing Before It", response.data)

    def test_scan_get(self):
        response = self.app.get('/scan')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Phishing URL Detector", response.data)

    def test_scan_post_safe_url(self):
        response = self.app.post('/scan', data={'url': 'https://www.google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SAFE WEBSITE", response.data)

    def test_scan_post_phishing_url(self):
        response = self.app.post('/scan', data={'url': 'http://paypal-login-security.xyz'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PHISHING", response.data)

if __name__ == "__main__":
    unittest.main()
