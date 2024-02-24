import unittest
from unittest.mock import patch
from app import app  # Import your Flask application


class TestUserServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("requests.get")  # Mock the requests.get call
    def test_get_with_valid_params(self, mock_get):
        # Mock the response from the Fibonacci Server
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = (
            "5"  # Assuming '5' is the expected Fibonacci number
        )

        # Perform the test
        response = self.app.get(
            "/fibonacci?hostname=fibonacci.com&fs_port=9090&number=5&as_ip=127.0.0.1&as_port=53533"
        )

        # Validate the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "5", response.data.decode()
        )  # Check if the Fibonacci number is in the response

    # Add more tests as needed


if __name__ == "__main__":
    unittest.main()
