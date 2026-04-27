# FastAPI Todo App

A simple Todo application built with FastAPI, SQLAlchemy, Jinja2 templates, and user authentication (JWT via OAuth2 password flow).

## Tech Stack
- FastAPI + Starlette (web framework)
- SQLAlchemy ORM (+ Alembic optional for migrations)
- Jinja2 (server-side templates) + static assets
- JWT via `python-jose` and password hashing via `passlib[bcrypt]`

## Prerequisites
- Python 3.10+ (tested with 3.13 locally)
- Optional: PostgreSQL 13+ if you want to use Postgres (default in code)
- Windows PowerShell or a Bash-compatible shell

## Clone the Repository

```bash
git clone https://github.com/Vijenderrr/todo-app-fast-api.git
cd todo-app-fast-api
```

## Create and Activate a Virtual Environment (Windows PowerShell)

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, you can install core packages directly:

```bash
pip install fastapi uvicorn[standard] SQLAlchemy alembic Jinja2 \
  passlib[bcrypt] python-jose[cryptography] python-multipart email-validator
```

## Database Configuration

The app is currently configured to use PostgreSQL in [TodoApp/database.py](TodoApp/database.py).

- Default DSN in code: `postgresql://postgres:pa$$word@localhost/TodoApplicationDatabase`
  - Note: In the code this is URL-encoded as `pa%24%24word` for `$`.
- Ensure PostgreSQL is running locally and the database exists:

```sql
-- In psql or a GUI like pgAdmin
CREATE DATABASE "TodoApplicationDatabase";
```

### Prefer SQLite for quick local runs?
Edit [TodoApp/database.py](TodoApp/database.py):

1) Uncomment the SQLite URL and engine lines, for example:

```python
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

2) Comment out the PostgreSQL lines. No other changes are required; tables are auto-created on startup.

## Run the App (Dev)

```bash
uvicorn TodoApp.main:app --reload
```

Open http://127.0.0.1:8000 to see the home page.

- Todos UI: http://127.0.0.1:8000/todos/todo-page (requires auth cookie)
- Auth pages:
  - Login: http://127.0.0.1:8000/auth/login-page
  - Register: http://127.0.0.1:8000/auth/register-page

Tip: After registering a user, use the login form to obtain a JWT cookie for accessing the todos page.

## Project Layout

- `TodoApp/main.py` – FastAPI app, routes mounting, templates setup
- `TodoApp/models.py` – SQLAlchemy models: `Users`, `Todos`
- `TodoApp/routers/` – Feature routers: `auth`, `todos`, `users`, `admin`
- `TodoApp/templates/` – Jinja2 HTML templates
- `TodoApp/static/` – CSS/JS assets
- `TodoApp/test/` – Pytest-based tests

## Running Tests (optional)

```bash
pip install pytest
pytest -q
```

## Common Issues

- Postgres connection error: verify the DSN in `TodoApp/database.py` and that the DB exists and is reachable.
- Missing dependencies: run `pip install -r requirements.txt` again or install the listed core packages.
- Windows PowerShell execution policy: if activation is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## License

This project is for educational purposes. Use at your discretion.
