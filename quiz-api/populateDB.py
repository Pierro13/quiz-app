import sqlite3
from models import Question, User
from datetime import datetime

def setup_test_db():
    # Connectez-vous à la base de données existante
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()

    # Créer la table User si elle n'existe pas déjà
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Exécutez une requête pour obtenir toutes les questions
    c.execute("SELECT * FROM questions")
    rows = c.fetchall()

    # Convertissez chaque ligne en un objet Question
    questions = [Question.from_row(row) for row in rows]

    # Ajouter des utilisateurs
    users = [
        User(id=1, username='TestUser1', date=datetime.now()),
        User(id=2, username='TestUser2', date=datetime.now()),
    ]
    for user in users:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, user.username, user.date))

    # Commit les changements
    conn.commit()

    # Fermez la connexion à la base de données
    conn.close()

    return questions, users

setup_test_db()