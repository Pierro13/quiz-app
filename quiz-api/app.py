from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import *
import jwt_utils
from models import Question, Answer
from database import add_question, get_db_connection, get_question_by_position

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

print("app.py is being executed")

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x} Jopel !"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    try:
        total_questions = get_total_number_of_questions()
        return jsonify({"total": total_questions}), 200
    except Exception as e:
        print(f"Error in /quiz-info: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/scores', methods=['GET'])
def GetScores():
    data = [user.to_dict() for user in get_all_users()]
    return jsonify(data), 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    password = payload['password']
    print(f"Password received: {password}")
    if password == 'flask2023': 
        token = jwt_utils.build_token()
        print(f"Token generated: {token}")
        return {"token": token}, 200
    else:
        return 'Unauthorized', 401

@app.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    question = Question(
        title=data.get('title'),
        text=data.get('text'),
        image=data.get('image'),
        position=data.get('position')
    )
    try:
        question_id = add_question(question)
        return jsonify({"id": question_id}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error in /questions POST: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    return "Ok", 200

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    try:
        return '', 204
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions_route():
    try:
        delete_all_questions()
        return '', 204
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = get_question_by_id(question_id)
        if question:
            return jsonify(question.to_dict()), 200
        else:
            return jsonify({"error": "Not Found"}), 404
    except Exception as e:
        print(f"Error in /questions/<int:question_id>: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        delete_question_by_id(question_id)
        return '', 204
    except Exception as e:
        print(f"Error in /questions/<int:question_id> DELETE: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions', methods=['GET'])
def get_question_by_position_route():
    position = request.args.get('position')
    print(f"Requested position: {position}")  # Ajoutez cette ligne pour déboguer
    try:
        question = get_question_by_position(position)
        if question:
            return jsonify(question.to_dict()), 200  # Ajoutez .to_dict() pour renvoyer un dictionnaire
        else:
            return jsonify({"error": "Not Found"}), 404
    except Exception as e:
        print(f"Error in /questions: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question_route(question_id):
    data = request.get_json()
    question = Question(
        title=data.get('title'),
        text=data.get('text'),
        image=data.get('image'),
        position=data.get('position')
    )
    try:
        update_question(question_id, question)
        return '', 204
    except Exception as e:
        print(f"Error in /questions/<int:question_id> PUT: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/quiz/end', methods=['POST'])
def end_quiz():
    try:
        data = request.get_json()
        score = data.get('score', 0)
        # Logic to handle end of the quiz, e.g., save score
        return jsonify({"message": "Quiz ended successfully", "score": score}), 200
    except Exception as e:
        print(f"Error in /quiz/end: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)
