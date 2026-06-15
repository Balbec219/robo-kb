from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    reports = conn.execute("SELECT * FROM reports").fetchall()
    conn.close()

    return render_template("index.html", reports=reports)

# ВАЖНО: Render не использует этот блок, но пусть будет
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
