"""Test the API endpoints"""
import unittest
import json
import os

from app.main import app

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

    def test_health_missing_data(self):
        """
        Test the health endpoint with missing data.
        
        This test ensures that the health endpoint can handle requests with missing data.
        """
        response = self.app.post('/health', headers={'x-api-key': self.test_api_key})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Data received and processed successfully')
        self.assertEqual(response.status_code, 200)

    def test_qr_missing_url(self):
        """
        Test the QR endpoint with missing URL.
        
        This test ensures that the QR endpoint returns an error when the URL is missing in the request data.
        """
        response = self.app.post('/qr', headers={'x-api-key': self.test_api_key}, json={})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'URL is missing')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
