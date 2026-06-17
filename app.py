from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db_connection()

    search = request.args.get("search", "")

    if search:
        reports = conn.execute(
            """
            SELECT * FROM reports
            WHERE title LIKE ?
            OR symptoms LIKE ?
            OR robot_model LIKE ?
            """,
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        reports = conn.execute(
            "SELECT * FROM reports ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        reports=reports,
        search=search
    )


@app.route("/create", methods=["GET", "POST"])
def create_report():

    if request.method == "POST":

        title = request.form["title"]
        robot_model = request.form["robot_model"]
        symptoms = request.form["symptoms"]
        cause = request.form["cause"]
        solution = request.form["solution"]
        status = request.form["status"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO reports
            (title, robot_model, symptoms, cause, solution, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                robot_model,
                symptoms,
                cause,
                solution,
                status
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("create.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
