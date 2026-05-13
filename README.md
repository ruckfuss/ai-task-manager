# 🤖 AI Task Manager

A full-stack task management web application powered by **Google Gemini AI**. 
Built with Python, Flask, and SQLite.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?logo=sqlite)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-orange?logo=google)

## ✨ Features

- **AI-Powered Analysis** — Each task is analyzed by Google Gemini, which provides a personalized productivity suggestion
- **Automatic Priority Detection** — AI classifies tasks as `high`, `medium`, or `low` priority automatically
- **Full CRUD Operations** — Add, complete, and delete tasks via a REST API
- **Persistent Storage** — All tasks stored in a local SQLite database
- **Responsive UI** — Clean dark-themed interface, works on all screen sizes

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite |
| AI | Google Gemini 1.5 Flash |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| API | RESTful endpoints |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### Installation

1. Clone the repository
```bash
   git clone https://github.com/ruckfuss/ai-task-manager.git
   cd ai-task-manager
```

2. Install dependencies
```bash
   pip install flask google-generativeai python-dotenv
```

3. Create a `.env` file in the root directory
GEMINI_API_KEY = AIzaSyDPpY-agAZxnmKp_cV2JnwKkq1QjCqhPQs

4. Run the application
```bash
   python app.py
```

5. Open your browser at `http://127.0.0.1:5000`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Fetch all tasks |
| POST | `/api/tasks` | Create a new task (triggers AI analysis) |
| PATCH | `/api/tasks/<id>/complete` | Mark a task as completed |
| DELETE | `/api/tasks/<id>` | Delete a task |

## 📁 Project Structure
ai-task-manager/
├── app.py              # Flask application & API routes
├── tasks.db            # SQLite database (auto-created)
├── .env                # API key (not committed)
├── templates/
│   └── index.html      # Main UI
└── static/
├── style.css       # Styling
└── app.js          # Frontend logic

## 📌 What I Learned

- Building REST APIs with Flask
- Integrating third-party AI APIs (Google Gemini)
- Database design and CRUD operations with SQLite
- Asynchronous JavaScript (fetch API)
- Environment variable management with dotenv
