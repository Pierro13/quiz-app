import sqlite3

def create_table():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position INTEGER NOT NULL UNIQUE,
        titre TEXT NOT NULL,
        texte TEXT NOT NULL,
        image TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_table()