# test_basic.py
import unittest
from app import create_app
from app.config import Testing

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = create_app(Testing)
        self.client = self.app.test_client()

    def test_home(self):
        # Send a request to the application
        response = self.client.get('/')
        # Check if the response is what we expect
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, world!')

if __name__ == '__main__':
    unittest.main()
