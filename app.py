
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"


# ------------------ DATABASE CONNECTION ------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------ CREATE TABLE ------------------
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        note TEXT
    )
    """)

    conn.commit()
    conn.close()


create_table()


# ------------------ HOME ROUTE ------------------
@app.route("/")
def index():
    conn = get_db_connection()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC"
    ).fetchall()

    total = conn.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0]

    category_data = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
    """).fetchall()

    monthly_data = conn.execute("""
        SELECT substr(date, 1, 7) AS month, SUM(amount) as total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """).fetchall()

    conn.close()   # ✅ CLOSE ONLY AFTER ALL QUERIES

    return render_template(
        "index.html",
        expenses=expenses,
        total=total if total else 0,
        category_data=category_data,
        monthly_data=monthly_data
    )

    
    


    return render_template(
        "index.html",
        expenses=expenses,
        total=total if total else 0,
        category_data=category_data
    )
    
    


# ------------------ ADD EXPENSE ------------------
@app.route("/add", methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]
    note = request.form["note"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note)
    )
    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/export/pdf")
def export_pdf():
    conn = get_db_connection()
    expenses = conn.execute(
        "SELECT date, category, amount, note FROM expenses ORDER BY date"
    ).fetchall()

    total = conn.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0] or 0

    conn.close()

    file_path = "expenses_report.pdf"

    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>Expense Report</b>", styles["Title"]))
    elements.append(Paragraph(f"Total Expense: ₹ {total}", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Table data
    table_data = [["Date", "Category", "Amount (₹)", "Note"]]

    for e in expenses:
        table_data.append([
            e["date"],
            e["category"],
            str(e["amount"]),
            e["note"] or ""
        ])

    table = Table(table_data, colWidths=[80, 100, 80, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    pdf.build(elements)

    return send_file(file_path, as_attachment=True)


# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)
