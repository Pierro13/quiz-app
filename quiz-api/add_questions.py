import sqlite3
from models import Question, Answer

def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            texte TEXT NOT NULL,
            image TEXT,
            position INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            texte TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            FOREIGN KEY (question_id) REFERENCES Questions(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_question(question):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Questions (titre, texte, image, position)
        VALUES (?, ?, ?, ?)
    ''', (question.title, question.text, question.image, question.position))
    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"Added question: {question.title} (ID: {question_id})")
    return question_id

def add_answer(answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Answers (question_id, texte, is_correct)
        VALUES (?, ?, ?)
    ''', (answer.question_id, answer.text, answer.is_correct))
    conn.commit()
    conn.close()

def main():
    create_tables()
    
    # Exemples de questions à ajouter
    questions = [
        Question(id=None, title="Question 1", text="What is the capital of France?", image="https://example.com/image1.jpg", position=1),
        Question(id=None, title="Question 2", text="What is 2 + 2?", image="https://example.com/image2.jpg", position=2),
        Question(id=None, title="Question 3", text="What is the color of the sky?", image="https://example.com/image3.jpg", position=3),
    ]

    for question in questions:
        question_id = add_question(question)
        
        # Ajoutez des réponses pour chaque question
        if question_id == 1:
            answers = [
                Answer(id=None, question_id=question_id, text="Paris", is_correct=True),
                Answer(id=None, question_id=question_id, text="London", is_correct=False),
                Answer(id=None, question_id=question_id, text="Berlin", is_correct=False),
                Answer(id=None, question_id=question_id, text="Madrid", is_correct=False)
            ]
        elif question_id == 2:
            answers = [
                Answer(id=None, question_id=question_id, text="3", is_correct=False),
                Answer(id=None, question_id=question_id, text="4", is_correct=True),
                Answer(id=None, question_id=question_id, text="5", is_correct=False),
                Answer(id=None, question_id=question_id, text="6", is_correct=False)
            ]
        elif question_id == 3:
            answers = [
                Answer(id=None, question_id=question_id, text="Blue", is_correct=True),
                Answer(id=None, question_id=question_id, text="Green", is_correct=False),
                Answer(id=None, question_id=question_id, text="Red", is_correct=False),
                Answer(id=None, question_id=question_id, text="Yellow", is_correct=False)
            ]

        for answer in answers:
            add_answer(answer)
            print(f"Added answer: {answer.text} for question ID: {question_id}")
    
    print("Questions and answers added to the database.")

if __name__ == "__main__":
    main()
