import sqlite3
from models import Question, User
from datetime import datetime

def clear_table(c, table):
    c.execute(f"DELETE FROM {table}")
    c.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

def setup_test_db():
    # Connectez-vous à la base de données existante
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()


    #clear_table(c, 'Users')

    # Créer la table User si elle n'existe pas déjà
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            score INTEGER DEFAULT 0
        )
    """)

    # Exécutez une requête pour obtenir toutes les questions
    c.execute("SELECT * FROM questions")
    rows = c.fetchall()

    # Convertissez chaque ligne en un objet Question
    questions = [Question.from_row(row) for row in rows]

    # Ajouter des utilisateurs
    users = [
        User(id=1, username='TestUser1', date=datetime.now(), score=10),
        User(id=2, username='TestUser2', date=datetime.now(), score=20),
        User(id=3, username='TestUser3', date=datetime.now(), score=30),
        User(id=4, username='TestUser4', date=datetime.now(), score=40),
        User(id=5, username='TestUser5', date=datetime.now(), score=50),
        User(id=6, username='TestUser6', date=datetime.now(), score=60),
    ]
    for user in users:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user.id, user.username, user.date, user.score))

    # Commit les changements
    conn.commit()

    # Fermez la connexion à la base de données
    conn.close()

    return questions, users

setup_test_db()