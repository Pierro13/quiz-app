from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x} and jopel and Pierro & MAX"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    sample_scores = [
        {"name": "John", "score": 100, "date": "2021-01-01"},
        {"name": "Jane", "score": 90, "date": "2021-01-02"},
        {"name": "Jim", "score": 80, "date": "2021-01-03"}
    ]
    return jsonify({"size": len(sample_scores), "scores": sample_scores}), 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    password = payload.get('password')

    if password == 'flask2023':
        token = b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'
        token_str = token.hex()
        return jsonify({"token": token_str}), 200
    else:
        return 'Unauthorized', 401

if __name__ == "__main__":
    app.run()
