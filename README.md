README.md

# todos_backend

Simple FastAPI backend for a Todo application with user registration, authentication, and per-user todo CRUD. It uses SQLAlchemy for persistence and Pydantic schemas for validation. Tables are created automatically on startup.

---

Table of contents
- What this is
- Stack
- Features
- Project structure
- How it fits together
- Environment
- Installation
- Run (development)
- Database initialization
- API (summary + examples)
- Models & Schemas
- Notes & development tips
- Contributing

What this is
------------
A small REST API service that provides user signup/login and CRUD operations for todos owned by users. Intended as the backend for a single-page Todo frontend (CORS configured for localhost dev and a Vercel frontend).

Stack
-----
- Language(s): Python 3.x
- Framework / runtime: FastAPI
- Notable libraries:
  - SQLAlchemy (ORM)
  - Pydantic (request/response validation)
  - python-dotenv (load environment variables)
  - fastapi[all] / uvicorn (ASGI server)

Features
--------
- User registration and authentication (token-based)
- Per-user todo items (title, description, completed flag)
- SQLAlchemy models and automatic table creation on startup
- CORS middleware configured for local dev and a specific frontend origin

Project structure (top-level)
-----------------------------
```
.gitignore
auth.py               # auth utilities (token creation / verification)
crud.py               # data access functions (create/read/update/delete)
database.py           # SQLAlchemy engine, SessionLocal, Base, create_session()
dependencies.py       # FastAPI dependency helpers (e.g., get_current_user)
eggrafes.py           # (Greek-named file; content for project-specific utilities)
main.py               # FastAPI app, CORS config, include routers, create_all()
models.py             # SQLAlchemy model definitions: User, Todo
requirements.txt      # Python dependencies
routers/              # FastAPI routers (users, todos)
schemas.py            # Pydantic request/response schemas
```

How it fits together
--------------------
- main.py creates the FastAPI app, applies CORS middleware and runs Base.metadata.create_all(bind=engine) to ensure tables exist, then includes routers from routers.users and routers.todos.
- database.py configures the SQLAlchemy engine using DATABASE_URL from environment variables and exposes a session factory and Base declarative base.
- models.py defines the User and Todo tables and their relationship (User.todos, Todo.owner).
- schemas.py defines request/response shapes used by endpoints (user creation, login responses, todo creation/update/response).
- auth.py, dependencies.py and crud.py implement authentication logic, dependencies for protected endpoints, and the CRUD operations against the DB; routers call those functions to handle HTTP requests.

Environment
-----------
The application expects environment variables loaded from a .env file or the environment:

- DATABASE_URL — SQLAlchemy database URL (example for SQLite: sqlite:///./test.db, or a Postgres URL like postgresql://user:pass@host:5432/dbname)

Installation
------------
1. Clone the repo:
   ```
   git clone https://github.com/kappa655/todos_backend.git
   cd todos_backend
   ```
2. Create a virtual environment and activate it (recommended):
   ```
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows (PowerShell)
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

Run (development)
-----------------
Start the app with uvicorn (typical for FastAPI development). From the project root:
```
uvicorn main:app --reload
```
- The app will create database tables automatically on startup (see main.py: Base.metadata.create_all(bind=engine)).
- CORS is configured in main.py to allow:
  - http://localhost:5173
  - https://todos-frontend-teal.vercel.app
  Adjust these origins in main.py if you use different frontends.

Database initialization
-----------------------
- Provide a valid DATABASE_URL environment variable. Example using SQLite (for quick local dev) in a `.env` file:
  ```
  DATABASE_URL=sqlite:///./todos.db
  ```
- On app start, SQLAlchemy will create the tables defined in models.py. For production we recommend using migrations (Alembic) instead of create_all.

API (summary + examples)
------------------------
The repository provides two router groups: users and todos. The exact path prefixes are defined in routers/*.py — below are typical endpoints and their request/response shapes inferred from the code (schemas.py). Check routers/ for the exact route paths and any additional parameters or prefixes.

Authentication
- Login returns a token response shaped like:
  ```json
  {
    "access_token": "<token string>",
    "token_type": "bearer"
  }
  ```
- Most todo endpoints are expected to be protected and require an Authorization header:
  ```
  Authorization: Bearer <access_token>
  ```

Typical user endpoints
- POST /users (or /users/register)
  - Body: UserCreate (username, email, password)
  - Creates a user and returns a UserResponse (id, username, email).
- POST /users/login (or /auth/token)
  - Body: UserLogin (email, password)
  - Returns: UserLoginResponse (access_token, token_type)

Typical todo endpoints (protected)
- GET /todos
  - Returns a list of TodoResponse objects.
- POST /todos
  - Body: TodoCreate (title, optional description)
  - Creates a todo for the authenticated user.
- GET /todos/{id}
  - Returns a single TodoResponse.
- PUT /todos/{id} or PATCH /todos/{id}
  - Body: TodoUpdate (title?, description?, completed?)
  - Updates the todo (only allowed for owner).
- DELETE /todos/{id}
  - Deletes the todo (only allowed for owner).

Example: register a user (curl)
```
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "s3cretpass"}'
```

Example: login and use token to create a todo
```
# 1) login -> get token
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "s3cretpass"}'

# assume response gives {"access_token":"<token>","token_type":"bearer"}

# 2) create a todo
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Buy milk", "description": "2 liters"}'
```

Models & Schemas (from code)
----------------------------
- models.py
  - User
    - id: Integer primary key
    - username: String(50)
    - email: String(50)
    - password: String(200)
    - created_at: DateTime server default now()
    - todos: relationship to Todo
  - Todo
    - id: Integer primary key
    - title: String(200)
    - description: String(200)
    - completed: Boolean (default False)
    - owner_id: ForeignKey to users.id (ondelete CASCADE)
    - owner: relationship to User

- schemas.py (Pydantic)
  - UserCreate: username, email, password (password uses SecretStr)
  - UserResponse: id, username, email
  - UserLogin / UserLoginResponse: email/password and access_token/token_type
  - TodoCreate: title, optional description
  - TodoUpdate: title?, description?, completed?
  - TodoResponse: id, title, description, completed

Notes & development tips
------------------------
- The app uses SQLAlchemy's create_all on startup. For production, switch to migrations (Alembic) to manage schema changes.
- Passwords in models are stored in a `password` column — auth.py likely contains password hashing and JWT/token generation utilities. Ensure secure password hashing (bcrypt/argon2) and secret management for tokens.
- The dependencies.py file likely includes a dependency to load the current user from the token; use that dependency in protected routes.
- If you change the CORS origins, update main.py.

Contributing
------------
- Issues and PRs welcome.
- Follow these steps for local development:
  1. Fork and clone.
  2. Create a feature branch.
  3. Implement code, add tests if applicable.
  4. Open a pull request describing changes.

Final notes
-----------
This README summarizes the repository structure and how to run and interact with the service based on the code found in main.py, database.py, models.py and schemas.py. For exact route paths, parameter names and additional behaviors, check the routers/ directory (routers/users.py and routers/todos.py) and the helper modules auth.py, crud.py and dependencies.py.