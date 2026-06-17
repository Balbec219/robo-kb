from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

SITE_VERSION = "1.1"

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
        OR tags LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )
    ).fetchall()

else:

    reports = conn.execute(
        "SELECT * FROM reports ORDER BY id DESC"
    ).fetchall()

conn.close()

return render_template(
    "index.html",
    reports=reports,
    search=search,
    version=SITE_VERSION
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
    tags = request.form.get("tags", "")

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO reports
        (
            title,
            robot_model,
            symptoms,
            cause,
            solution,
            status,
            tags
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            robot_model,
            symptoms,
            cause,
            solution,
            status,
            tags
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")

return render_template("create.html")

@app.route("/report/"int:report_id" (int:report_id)")
def report_page(report_id):

conn = get_db_connection()

report = conn.execute(
    "SELECT * FROM reports WHERE id = ?",
    (report_id,)
).fetchone()

conn.close()

if report is None:
    return "Отчёт не найден", 404

return render_template(
    "report.html",
    report=report,
    version=SITE_VERSION
)

@app.route("/delete/"int:report_id" (int:report_id)", methods=["POST"])
def delete_report(report_id):

conn = get_db_connection()

conn.execute(
    "DELETE FROM reports WHERE id = ?",
    (report_id,)
)

conn.commit()
conn.close()

return redirect("/")

if __name__ == "__main__":
app.run(
host="0.0.0.0",
port=int(os.environ.get("PORT", 5000))
)
