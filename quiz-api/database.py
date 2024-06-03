import sqlite3
from models import Question

def get_db_connection():
    connexion = sqlite3.connect('quiz.db')
    connexion.row_factory = sqlite3.Row
    return connexion

def add_question(question):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Questions WHERE position = ?', (question.position,))
    existing_question = cursor.fetchone()

    if existing_question:
        connection.close()
        raise sqlite3.IntegrityError("Question with this position already exists.")

    cursor.execute('INSERT INTO Questions (titre, texte, image, position) VALUES (?, ?, ?, ?)', (question.title, question.text, question.image, question.position))
    connection.commit()
    question_id = cursor.lastrowid
    connection.close()
    return question_id

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

def delete_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Questions')
    conn.commit()
    conn.close()

def get_question_by_position(position):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Questions WHERE position = ?', (position,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Question.from_row(row)
    else:
        return None
    
def update_question(question):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Questions SET titre = ?, texte = ?, image = ?, position = ? WHERE id = ?', (question.title, question.text, question.image, question.position, question.id))
    conn.commit()
    conn.close()

def delete_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()


##################################### USERS #####################################
import json
from models import User

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()
    conn.close()
    return [User(id=row['id'], username=row['username'], date=row['date']) for row in rows]