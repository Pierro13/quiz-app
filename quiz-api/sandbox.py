import sqlite3

def add_code_column():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE Questions ADD COLUMN code TEXT")
    conn.commit()
    conn.close()

#add_code_column()

def create_table():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Participations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            answers TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

