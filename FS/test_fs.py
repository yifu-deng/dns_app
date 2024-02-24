import unittest
import requests


class TestFibonacciServer(unittest.TestCase):
    BASE_URL = "http://localhost:9090/fibonacci"

    def test_fibonacci_valid_number(self):
        params = {"number": "5"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["Fibonacci"], 5
        )  # Assuming the Fibonacci service returns a JSON response

    def test_fibonacci_invalid_number(self):
        params = {"number": "invalid"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
