python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    a = data["a"]
    b = data["b"]
    return jsonify({"result": a + b})

@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.get_json()
    a = data["a"]
    b = data["b"]
    return jsonify({"result": a - b})

@app.route("/divide", methods=["POST"])
def divide():
    data = request.get_json()
    a = data["a"]
    b = data["b"]
    if b == 0:
        return jsonify({"error": "Cannot divide by zero"})
    else:
        return jsonify({"result": a / b})

@app.route("/multiply", methods=["POST"])
def multiply():
    data = request.get_json()
    a = data["a"]
    b = data["b"]
    return jsonify({"result": a * b})

if __name__ == "__main__":
    app.run(debug=True)