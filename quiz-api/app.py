from flask import Flask, request
from flask_cors import CORS
import jwt_utils
from models import Question
from database import add_question, get_db_connection

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    password = payload['password']
    if password == 'correct_password':
        token = jwt_utils.build_token()
        return {"token": token}, 200
    else:
        return 'Unauthorized', 401

@app.route('/questions', methods=['POST'])
def create_question():
    token = request.headers.get('Authorization')
    if not token or not jwt_utils.verify_token(token):
        return 'Unauthorized', 401

    data = request.get_json()
    question = Question(
        id=None,
        title=data['title'],
        text=data['text'],
        image=data['image'],
        position=data['position']
    )

    question = add_question(question)
    return question.to_dict(), 201

if __name__ == "__main__":
    app.run()
