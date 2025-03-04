import unittest
from app import app
from flask import json

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_division_by_zero(self):
        response = self.app.post('/calculate', data=json.dumps(dict(num1=10, num2=0, operator='/')), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot divide by zero', str(response.data))

    def test_invalid_operator(self):
        response = self.app.post('/calculate', data=json.dumps(dict(num1=5, num2=3, operator='
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid operator: Please use +, -, *, or /', str(response.data))
        
    def test_invalid_input_non_numeric(self):
        response = self.app.post('/calculate', data=json.dumps(dict(num1='abc', num2=3, operator='+')), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input: Please enter numeric values', str(response.data))

if __name__ == "__main__":
    unittest.main()