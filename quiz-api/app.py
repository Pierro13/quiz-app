from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import *
import jwt_utils
from models import Question, Answer
from datetime import datetime
from PIL import Image
from io import BytesIO
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
import os

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
        print(f"Total questions: {total_questions}")

        participations = get_all_participations_list()
        print(f"Participations: {participations}")

        if not participations:
            return jsonify({"size": total_questions, "scores": []}), 200

        # Calculer les scores pour chaque participation
        for participation in participations:
            score = calculate_score(participation)
            participation['score'] = score

        # Trier les participations par score décroissant
        sorted_participations = sorted(participations, key=lambda x: x['score'], reverse=True)
        print(f"Sorted participations: {sorted_participations}")

        return jsonify({"size": total_questions, "scores": sorted_participations}), 200
    except Exception as e:
        print(f"Error in /quiz-info: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    
def calculate_score(participation):
    answers = participation['answers']
    print(f"Calculating score for answers: {answers}")
    score = 0
    questions = get_all_questions()
    
    for question in questions:
        question.answers = get_answers_by_question_id(question.id)

    if not questions:
        print("No questions found.")
        return 0

    for i, answer_index in enumerate(answers):
        if i >= len(questions):
            print(f"Answer index {i} is out of range for questions.")
            break
        question = questions[i]
        print(f"Processing question {i+1}/{len(questions)} with ID: {question.id}")
        correct_answer = next((a for a in question.answers if a.is_correct), None)
        chosen_answer = question.answers[answer_index - 1] if answer_index > 0 else None
        if correct_answer and chosen_answer:
            print(f"Correct answer ID: {correct_answer.id}, Chosen answer ID: {chosen_answer.id}")
            if correct_answer.id == chosen_answer.id:
                score += 1

    print(f"Calculated score: {score}")
    return score


@app.route('/scores', methods=['GET'])
def GetScores():
    data = [user.to_dict() for user in get_all_users()]
    return jsonify(data), 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if payload is None:
        return 'Bad Request: No JSON data found', 400
    password = payload.get('password')
    if password is None:
        return 'Bad Request: No password found', 400
    print(f"Password received: {password}")
    if password == 'flask2023': 
        token = jwt_utils.build_token()
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        print(f"Token generated: {token}")
        return {"token": token}, 200
    else:
        return 'Unauthorized', 401

    
def is_logged():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) == 2 else None
    if not token or not jwt_utils.verify_token(token):
        return False
    return True

@app.route('/check-token-validity', methods=['GET'])
def check_token_validity():
    if is_logged():
        return {"valid": True}, 200
    return {"valid": False}, 401


@app.route('/questions', methods=['POST'])
def create_question():
    if not is_logged():
        return 'Unauthorized', 401
    
    data = request.get_json()
    
    code = data.get('code')
    
    question = Question(
        id=data.get('id'),
        title=data.get('title'),
        text=data.get('text'),
        image=data.get('image'),
        position=data.get('position'),
        code=code
    )
    
    answers = data.get('possibleAnswers', [])
    
    try:
        # if question.code:
        #     output_path = f"static/code_images/question_{question.position}.webp"
        #     generate_code_image(question.code, output_path)
        #     question.image = output_path
        
        question_id = add_question(question)
        
        for answer in answers:
            answer_obj = Answer(
                id=None,
                question_id=question_id,
                text=answer['text'],
                is_correct=answer['isCorrect']
            )
            add_answer(answer_obj)
        
        return jsonify({"id": question_id}), 200
    
    except sqlite3.IntegrityError as e:
        if "Question with this position already exists" in str(e):
            return jsonify({"error": "Position is already taken. Please choose a different one."}), 400
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        print(f"Error in /questions POST: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    return "Ok", 200

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations_route():
    try:
        delete_all_participations()
        return '', 204
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@app.route('/participations', methods=['POST'])
def add_participation_route():
    data = request.get_json()
    player_name = data.get('playerName')
    answers = data.get('answers')

    if not player_name or not answers:
        return jsonify({'Error': 'Player name and answers are required.'}), 400

    # Vérifiez le nombre total de réponses par rapport au nombre de réponses données par le joueur
    total_questions = get_total_number_of_questions()
    if len(answers) != total_questions:
        return jsonify({'Error': 'The number of answers provided does not match the number of questions.'}), 400

    # Calculer le score en fonction des réponses correctes
    score = 0
    for question_position, answer_index in enumerate(answers, start=1):
        question = get_question_by_position(question_position)
        if question:
            possible_answers = get_answers_by_question_id(question.id)
            if answer_index is not None:
                if 0 <= answer_index - 1 < len(possible_answers):
                    chosen_answer = possible_answers[answer_index - 1]
                    if chosen_answer.is_correct:
                        score += 1

    try:
        participation = Participation(None, player_name, json.dumps(answers))
        add_participation_to_db(participation)
        return jsonify({
            'playerName': player_name,
            'score': score,
            'answers': answers
        }), 200
    except Exception as e:
        print(f"Error in /participations POST: {e}")
        return jsonify({'Error': 'An unexpected error occurred.'}), 500


@app.route('/participations', methods=['GET'])
def get_all_participations_route():
    try:
        participations = get_all_participations_list()
        return jsonify(participations), 200
    except Exception as e:
        print(f"Error in /participations GET: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions_route():
    if is_logged() == False:
        return 'Unauthorized', 401
    try:
        delete_all_questions()
        return 'All questions have been deleted', 204
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@app.route('/questions/all', methods=['GET'])
def get_all_questions_route():
    try:
        questions = get_all_questions()
        questions_with_answers = []
        for question in questions:
            question_dict = question.to_dict()
            question_dict['possibleAnswers'] = [answer.to_dict() for answer in get_answers_by_question_id(question.id)]
            questions_with_answers.append(question_dict)
        print("Questions with answers:", questions_with_answers)
        return jsonify(questions_with_answers), 200
    except Exception as e:
        print(f"Error in /questions/all: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = get_question_by_id(question_id)
        if question:
            question_dict = question.to_dict()
            question_dict['possibleAnswers'] = [
                answer.to_dict() for answer in get_answers_by_question_id(question.id)
            ]
            return jsonify(question_dict), 200
        else:
            return jsonify({"error": "Not Found"}), 404
    except Exception as e:
        print(f"Error in /questions/<int:question_id>: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    if is_logged() == False:
        return 'Unauthorized', 401
    try:
        if not get_question_by_id(question_id):
            return 'Question not found', 404
        delete_question_by_id(question_id)
        return '', 204
    except Exception as e:
        print(f"Error in /questions/<int:question_id> DELETE: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions', methods=['GET'])
def get_question_by_position_route():
    position = request.args.get('position')
    print(f"Requested position: {position}")
    try:
        question = get_question_by_position(position)
        if question:
            question_dict = question.to_dict()
            question_dict['possibleAnswers'] = [answer.to_dict() for answer in get_answers_by_question_id(question.id)]
            return jsonify(question_dict), 200
        else:
            return jsonify({"error": "Not Found"}), 404
    except Exception as e:
        print(f"Error in /questions: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question_route(question_id):
    data = request.get_json()
    question = Question(
        id=question_id,
        title=data.get('title'),
        text=data.get('text'),
        image=data.get('image'),
        position=data.get('position'),
        code=data.get('code')
    )
    answers = data.get('possibleAnswers', [])

    try:
        if not get_question_by_id(question_id):
            return 'Question not found', 404
        if question.code:
            output_path = f"static/code_images/question_{question.position}.webp"
            generate_code_image(question.code, output_path)
            question.image = output_path
        

        update_question(question_id, question)

        # Supprimer les anciennes réponses
        delete_answers_by_question_id(question_id)

        # Ajouter les nouvelles réponses
        for answer in answers:
            answer_obj = Answer(
                id=None,
                question_id=question_id,
                text=answer['text'],
                is_correct=answer['isCorrect']
            )
            add_answer(answer_obj)
        
        return 'Question updated', 204
    except Exception as e:
        print(f"Error in /questions/<int:question_id> PUT: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/quiz/end', methods=['POST'])
def end_quiz():
    try:
        data = request.get_json()
        score = data.get('score', 0)
        return jsonify({"message": "Quiz ended successfully", "score": score}), 200
    except Exception as e:
        print(f"Error in /quiz/end: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answer_id = data.get('answer_id')

    print(f"Request received: {data}")

    if answer_id is None:
        return jsonify({"error": "Answer ID is required"}), 400

    try:
        answer = get_answer_by_id(answer_id)
        if answer:
            question = get_question_by_id(answer.question_id)
            if question:
                correct_answer = next((a for a in get_answers_by_question_id(question.id) if a.is_correct), None)
                if correct_answer and correct_answer.id == answer_id:
                    print(f"Answer {answer_id} is correct.")
                    return jsonify({"correct": True, "score": 1}), 200
                else:
                    print(f"Answer {answer_id} is incorrect.")
                    return jsonify({"correct": False, "score": 0}), 200
            else:
                print(f"Question not found for answer {answer_id}.")
                return jsonify({"error": "Question not found"}), 404
        else:
            print(f"Answer {answer_id} not found.")
            return jsonify({"error": "Answer not found"}), 404
    except Exception as e:
        print(f"Error in /submit-answer: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

    
@app.route('/add-user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    print("Data received:", data)
    username = data.get('username')
    score = data.get('score')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        add_user(username, date, score)
        return jsonify({'Success': 'User added successfully'}), 201
    except Exception as e:
        print(f"Error in /add-user: {e}")
        return jsonify({'Error': 'An unexpected error occurred.'}), 500

def generate_code_image(code, output_path):
    font_path = 'DejaVuSerif.ttf'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    lexer = PythonLexer()
    formatter = ImageFormatter(font_name=font_path, line_numbers=True)
    img_data = highlight(code, lexer, formatter)
    image = Image.open(BytesIO(img_data))
    image.save(output_path, format='WEBP')

if __name__ == '__main__':
    app.run(debug=True)
