"""Test the API endpoints"""
import unittest
import json

from app.main import app

class TestAPI(unittest.TestCase):
    """Test the API endpoints"""

    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get('/')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Hello, World!')

    def test_get_data(self):
        response = self.app.get('/api/data')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {'key': 'value'})

    def test_post_data(self):
        response = self.app.post('/api/data', json={'key': 'value'})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Data received and processed successfully')

if __name__ == '__main__':
    unittest.main()
