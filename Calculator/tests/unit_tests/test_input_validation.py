import unittest
import re
from flask import Flask, request
app = Flask(__name__)

@app.route('/validate_input', methods=['POST'])
def validate_input():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operator = request.form.get('operator')
    
    if not re.match("^[0-9]+(\.[0-9]{1,2})?$", num1) or not re.match("^[0-9]+(\.[0-9]{1,2})?$", num2):
        return {"status": "error", "message": "Invalid input: Please enter numeric values"}
    
    if operator not in ['+', '-', '*', '/']:
        return {"status": "error", "message": "Invalid operator: Please use +, -, *, or /"}
    
    if operator == '/' and num2 == '0':
        return {"status": "error", "message": "Cannot divide by zero"}
    
    return {"status": "success"}

class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_validate_input(self):
        response = self.app.post('/validate_input', data=dict(num1='abc', num2='3', operator='+'))
        self.assertEqual(response.get_json(), {"status": "error", "message": "Invalid input: Please enter numeric values"})

        response = self.app.post('/validate_input', data=dict(num1='5', num2='3', operator='
        self.assertEqual(response.get_json(), {"status": "error", "message": "Invalid operator: Please use +, -, *, or /"})

        response = self.app.post('/validate_input', data=dict(num1='10', num2='0', operator='/'))
        self.assertEqual(response.get_json(), {"status": "error", "message": "Cannot divide by zero"})

        response = self.app.post('/validate_input', data=dict(num1='5', num2='3', operator='+'))
        self.assertEqual(response.get_json(), {"status": "success"})

if __name__ == '__main__':
    unittest.main()