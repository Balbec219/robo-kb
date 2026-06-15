from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Главная страница + поиск
@app.route("/")
def home():
    search = request.args.get("search")

    conn = get_db_connection()

    if search:
        query = """
        SELECT * FROM reports
        WHERE title LIKE ? OR robot_model LIKE ? OR symptoms LIKE ?
        ORDER BY id DESC
        """
        reports = conn.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        reports = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()

    conn.close()

    return render_template("index.html", reports=reports, search=search)

# Создание отчёта
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        robot_model = request.form["robot_model"]
        symptoms = request.form["symptoms"]
        cause = request.form["cause"]
        solution = request.form["solution"]
        status = request.form["status"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO reports (title, robot_model, symptoms, cause, solution, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, robot_model, symptoms, cause, solution, status))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("create.html")

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
