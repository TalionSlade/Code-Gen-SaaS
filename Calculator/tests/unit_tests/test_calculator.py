import unittest
from calculator import app

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_addition(self):
        result = self.app.post('/calculate', data=dict(num1=5, num2=3, operator='+'))
        self.assertEqual(result.data, 8)

    def test_subtraction(self):
        result = self.app.post('/calculate', data=dict(num1=10, num2=4, operator='-'))
        self.assertEqual(result.data, 6)

    def test_multiplication(self):
        result = self.app.post('/calculate', data=dict(num1=7, num2=6, operator='*'))
        self.assertEqual(result.data, 42)

    def test_division(self):
        result = self.app.post('/calculate', data=dict(num1=20, num2=5, operator='/'))
        self.assertEqual(result.data, 4)

    def test_division_by_zero(self):
        result = self.app.post('/calculate', data=dict(num1=10, num2=0, operator='/'))
        self.assertEqual(result.data, "Cannot divide by zero")

    def test_invalid_input(self):
        result = self.app.post('/calculate', data=dict(num1='abc', num2=3, operator='+'))
        self.assertEqual(result.data, "Invalid input: Please enter numeric values")

    def test_invalid_operator(self):
        result = self.app.post('/calculate', data=dict(num1=5, num2=3, operator='#'))
        self.assertEqual(result.data, "Invalid operator: Please use +, -, *, or /")

    def test_decimal_numbers(self):
        result = self.app.post('/calculate', data=dict(num1=5.5, num2=3.2, operator='+'))
        self.assertEqual(result.data, 8.7)

if __name__ == "__main__":
    unittest.main()