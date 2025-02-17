from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to my calculator API!'

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    num1 = float(data['num1'])
    num2 = float(data['num2'])
    result = num1 + num2
    return jsonify({'result': result})

@app.route('/subtract', methods=['POST'])
def subtract():
    data = request.get_json()
    num1 = float(data['num1'])
    num2 = float(data['num2'])
    result = num1 - num2
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide():
    data = request.get_json()
    num1 = float(data['num1'])
    num2 = float(data['num2'])
    result = num1 / num2
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    num1 = float(data['num1'])
    num2 = float(data['num2'])
    result = num1 * num2
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)