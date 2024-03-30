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

if __name__ == '__main__':
    unittest.main()
