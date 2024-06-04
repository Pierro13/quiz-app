import sqlite3
from models import Question, Answer, User

def get_db_connection():
    connexion = sqlite3.connect('quiz.db')
    connexion.row_factory = sqlite3.Row
    return connexion

def add_question(question):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Questions WHERE position = ?', (question.position,))
    existing_question = cursor.fetchone()

    if existing_question:
        conn.close()
        raise sqlite3.IntegrityError("Question with this position already exists.")

    cursor.execute('INSERT INTO Questions (titre, texte, image, position, code) VALUES (?, ?, ?, ?, ?)', 
                   (question.title, question.text, question.image, question.position, question.code))
    conn.commit()
    question_id = cursor.lastrowid
    conn.close()
    return question_id


def get_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Questions')
    rows = cursor.fetchall()
    conn.close()
    return [Question.from_row(row) for row in rows]

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
    if row:
        question = Question.from_row(row)
        question.answers = get_answers_by_question_id(question.id)
        conn.close()
        return question
    conn.close()
    return None
    
def get_total_number_of_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Questions')
    total = cursor.fetchone()[0]
    conn.close()
    return total

def update_question(question_id, question):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Questions SET titre = ?, texte = ?, image = ?, position = ? WHERE id = ?', (question.title, question.text, question.image, question.position, question_id))
    conn.commit()
    conn.close()

def update_question_positions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Questions ORDER BY position')
    rows = cursor.fetchall()
    position = 1
    for row in rows:
        cursor.execute('UPDATE Questions SET position = ? WHERE id = ?', (position, row['id']))
        position += 1
    conn.commit()
    conn.close()

def delete_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    update_question_positions()

def add_answer(answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Answers (question_id, texte, is_correct)
        VALUES (?, ?, ?)
    ''', (answer.question_id, answer.text, answer.is_correct))
    conn.commit()
    conn.close()

def get_answers_by_question_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Answers WHERE question_id = ?', (question_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Answer.from_row(row) for row in rows]

def get_answer_by_id(answer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Answers WHERE id = ?', (answer_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Answer.from_row(row)
    else:
        return None


import json
from models import User

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()
    conn.close()
    return [User(id=row['id'], username=row['username'], date=row['date'], score=row['score']) for row in rows]

def add_user(username, date, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
                    INSERT INTO Users (username, date, score)
                   VALUES (?, ?, ?)         
                   ''', (username, date, score))
    conn.commit()
    conn.close()

