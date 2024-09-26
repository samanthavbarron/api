"""Test the API endpoints"""
import unittest
import json
import os

from app.main import app, AppConfig, QRCode, check_api_key, require_api_key

class TestAPI(unittest.TestCase):
    """Test the API endpoints"""

    def setUp(self):
        self.app = app.test_client()
        self.test_api_key = "test_key_123"
        os.environ['API_KEY'] = self.test_api_key

    def test_health_bad(self):
        """Test the health endpoint"""
        response = self.app.post('/health', headers={'x-api-key': 'wrong_key'})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'API key is missing or incorrect')
        self.assertEqual(response.status_code, 403)

    def test_health_good(self):
        response = self.app.post('/health', headers={'x-api-key': self.test_api_key}, json={'test': 'data'})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Data received and processed successfully')
        self.assertEqual(response.status_code, 200)
    
    def test_qr_bad(self):
        response = self.app.post('/qr', headers={'x-api-key': 'wrong_key'})
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', data)
    
    def test_qr_good(self):
        response = self.app.post('/qr', headers={'x-api-key': self.test_api_key}, json={'url': 'http://example.com'})
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)
        self.assertEqual(response.status_code, 200)
    
    def test_qr_redirect(self):
        response = self.app.get('/qr')
        self.assertEqual(response.status_code, 302)
        self.assertIn(
            ".com",
            response.location
        )

        response = self.app.post('/qr', headers={'x-api-key': self.test_api_key}, json={'url': 'http://new_url.com'})
        self.assertIn('new_url.com', response.get_json()["new_url"])

    def test_app_config(self):
        config = AppConfig(host="localhost", port=5000, debug=True)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 5000)
        self.assertTrue(config.debug)

    def test_qr_code(self):
        qr = QRCode(url="http://example.com", mode="test")
        self.assertEqual(qr.url, "http://example.com")
        self.assertEqual(qr.mode, "test")

    def test_check_api_key_valid(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['x-api-key'] = self.test_api_key
            request = client.post('/health', headers={'x-api-key': self.test_api_key})
            self.assertTrue(check_api_key(request, key_name="main"))

    def test_check_api_key_invalid(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['x-api-key'] = 'invalid_key'
            request = client.post('/health', headers={'x-api-key': 'invalid_key'})
            self.assertFalse(check_api_key(request, key_name="main"))

    def test_require_api_key_decorator_valid(self):
        @require_api_key(api_key_name="main")
        def dummy_function():
            return "Success"

        with self.app as client:
            with client.session_transaction() as sess:
                sess['x-api-key'] = self.test_api_key
            request = client.post('/health', headers={'x-api-key': self.test_api_key})
            response = dummy_function()
            self.assertEqual(response, "Success")

    def test_require_api_key_decorator_invalid(self):
        @require_api_key(api_key_name="main")
        def dummy_function():
            return "Success"

        with self.app as client:
            with client.session_transaction() as sess:
                sess['x-api-key'] = 'invalid_key'
            request = client.post('/health', headers={'x-api-key': 'invalid_key'})
            response = dummy_function()
            self.assertEqual(response[1], 403)

    def test_health_missing_data(self):
        response = self.app.post('/health', headers={'x-api-key': self.test_api_key})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Data received and processed successfully')
        self.assertEqual(response.status_code, 200)

    def test_qr_missing_url(self):
        response = self.app.post('/qr', headers={'x-api-key': self.test_api_key}, json={})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'URL is missing')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
