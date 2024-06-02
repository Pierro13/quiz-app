import sqlite3
from models import Question

def get_db_connection():
    connexion = sqlite3.connect('quiz.db')
    connexion.row_factory = sqlite3.Row
    return connexion

def add_question(question):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Questions (titre, texte, image, position) VALUES (?, ?, ?, ?)',(question.title, question.text, question.image, question.position))
    conn.commit()
    question.id = cursor.lastrowid
    conn.close()
    return question

def get_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Questions WHERE id = ?', (question_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Question.from_row(row)
    else:
        return None
