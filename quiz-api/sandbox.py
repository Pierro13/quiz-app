import sqlite3

def add_code_column():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE Questions ADD COLUMN code TEXT")
    conn.commit()
    conn.close()

add_code_column()
