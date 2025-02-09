from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add():
    num1 = float(request.json['num1'])
    num2 = float(request.json['num2'])
    result = num1 + num2
    return jsonify({'result': result})

@app.route('/subtract', methods=['POST'])
def subtract():
    num1 = float(request.json['num1'])
    num2 = float(request.json['num2'])
    result = num1 - num2
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide():
    num1 = float(request.json['num1'])
    num2 = float(request.json['num2'])
    if num2 == 0:
        return 'Error: Division by zero is not allowed.', 400
    result = num1 / num2
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply():
    num1 = float(request.json['num1'])
    num2 = float(request.json['num2'])
    result = num1 * num2
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)