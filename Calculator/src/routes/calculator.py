from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    try:
        num1 = float(data.get('num1'))
        num2 = float(data.get('num2'))
        operator = data.get('operator')

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return jsonify({"error": "Cannot divide by zero"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operator: Please use +, -, *, or /"}), 400

    except ValueError:
        return jsonify({"error": "Invalid input: Please enter numeric values"}), 400

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)