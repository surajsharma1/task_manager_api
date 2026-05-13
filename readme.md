# Task Manager API

> A production-deployed RESTful API built with Python and Flask. Supports full task CRUD operations with JWT-based authentication and PostgreSQL persistence.

🔗 **Live (Render):** `https://your-app.onrender.com`  
🔗 **Live (PythonAnywhere):** `https://yourusername.pythonanywhere.com`

---

## What This Is

A backend REST API for managing tasks per user. Built to demonstrate real-world Flask patterns — authentication, protected routes, database integration, and clean project structure. Deployed on two platforms (Render and PythonAnywhere).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| Framework | Flask |
| Database | PostgreSQL (production), SQLite (development) |
| Auth | JWT via PyJWT |
| DB Driver | psycopg2 |
| Deployment | Render, PythonAnywhere |

---

## API Endpoints

### Auth

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login, returns JWT token |

### Tasks

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/tasks` | Yes | Get all tasks for logged-in user |
| POST | `/tasks` | Yes | Create a new task |
| GET | `/tasks/<id>` | Yes | Get a specific task |
| PUT | `/tasks/<id>` | Yes | Update a task |
| DELETE | `/tasks/<id>` | Yes | Delete a task |

> All `/tasks` routes require `Authorization: Bearer <your_jwt_token>` in the request header.

---

## Example Requests

### Register
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "suraj",
  "password": "yourpassword"
}
```

### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "suraj",
  "password": "yourpassword"
}

# Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Create Task (Protected)
```bash
POST /tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Complete README",
  "description": "Write proper docs",
  "status": "pending"
}
```

---

## Project Structure

```
task-manager-api/
├── app.py               # App factory / entry point
├── auth.py              # Register, login, JWT generation
├── tasks.py             # Task CRUD route handlers
├── db.py                # Database connection (psycopg2)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md
```

---

## Local Setup

### Prerequisites
- Python 3.8+
- PostgreSQL installed and running (or use SQLite for local dev)

### Installation

```bash
git clone https://github.com/surajsharma1/task-manager-api.git
cd task-manager-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your DB credentials and JWT secret
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/taskdb
JWT_SECRET=your_secret_key_here
FLASK_ENV=development
```

### Run Locally

```bash
python app.py
```

API runs at `http://localhost:5000`

---

## Database Migration Note

This project was originally built with **SQLite** and later migrated to **PostgreSQL** for production deployment.

Key differences handled during migration:
- Placeholder syntax: SQLite uses `?`, psycopg2 uses `%s`
- Row access: SQLite rows support both index and key access; psycopg2 returns tuples by default (use `RealDictCursor` for dict-style access)
- Connection handling: psycopg2 requires explicit `conn.commit()` for write operations

---

## Deployment

### Render
- Add a PostgreSQL database from Render dashboard
- Set environment variables in Render settings
- Deploy via GitHub integration (auto-deploys on push)

### PythonAnywhere
- Upload project files via the Files tab or git clone
- Set environment variables in the WSGI config
- Configure the WSGI file to point to your Flask app

---

## Author

**Suraj Sharma**  
B.Tech IT — Malwa Institute of Science & Technology, Indore  
[github.com/surajsharma1](https://github.com/surajsharma1)
