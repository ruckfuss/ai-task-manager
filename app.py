from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT DEFAULT 'medium',
        ai_suggestion TEXT,
        completed INTEGER DEFAULT 0,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY completed ASC, created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"error": "Title required"}), 400

    # Gemini'den öneri al
    prompt = f"""You are a productivity assistant. Analyze this task and give a SHORT (max 2 sentences) actionable suggestion on how to approach it efficiently.

Task: {title}
Description: {description if description else 'No description'}

Respond in the same language as the task title. Be concise and practical."""

    try:
        response = model.generate_content(prompt)
        ai_suggestion = response.text.strip()
    except Exception:
        ai_suggestion = "AI suggestion unavailable."

    # Öncelik tahmini
    priority_prompt = f"""Classify this task priority as exactly one word: 'high', 'medium', or 'low'.
Task: {title}. Respond with only the single word."""
    try:
        p_response = model.generate_content(priority_prompt)
        priority = p_response.text.strip().lower()
        if priority not in ["high", "medium", "low"]:
            priority = "medium"
    except Exception:
        priority = "medium"

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, description, priority, ai_suggestion, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, description, priority, ai_suggestion, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added successfully"}), 201

@app.route("/api/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task completed"})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)