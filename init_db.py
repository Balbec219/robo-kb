import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    robot_model TEXT,
    symptoms TEXT,
    cause TEXT,
    solution TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("База данных создана!")
