from flask import Flask, request
from flask_cors import CORS
import sqlite3
import jwt_utils

app = Flask(__name__)
CORS(app)

def get_db_connection():
    connexion = sqlite3.connect('bdd.db')
    connexion.row_factory = sqlite3.Row
    return connexion

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x} and jopel and Pierro & MAX"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200


#b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'

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
    title = data['title']
    text = data['text']
    image = data['image']
    position = data['position']

    connexion = get_db_connection()
    cursor = connexion.cursor()
    cursor.execute('INSERT INTO Questions (titre, texte, image, position) VALUES (?, ?, ?, ?)',(title, text, image, position))
    connexion.commit()
    connexion.close()

    return {'id': cursor.lastrowid, 'title': title, 'text': text, 'image': image, 'position': position}, 201

if __name__ == "__main__":
    app.run()
