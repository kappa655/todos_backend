README.md

# todos_backend

FastAPI backend for a Todo application with user registration, user login, authentication, and per-user todo CRUD. A user can create, read, update and delete notes.

---

Table of contents
- Stack
- Features
- Project structure
- How it fits together
- Environment
- Installation
- Run (development)
- Database initialization
- API
- Models & Schemas

Stack
-----
- Language: Python
- Framework: FastAPI
- Notable libraries:
  - SQLAlchemy (ORM)
  - Pydantic (request/response validation)
  - uvicorn (ASGI server)

Features
--------
- User registration and authentication (token-based)
- Per-user todo items (title, description, completed flag)
- SQLAlchemy models and automatic table creation on startup
- CORS middleware configured for local dev and a vercel as frontend

Project structure (top-level)
-----------------------------
```
.gitignore
auth.py               # auth utilities (token creation / verification)
database.py           # SQLAlchemy engine, SessionLocal, Base, create_session()
dependencies.py       # FastAPI dependency helpers (e.g. get_current_user)
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
- auth.py, dependencies.py implement authentication logic, dependencies for protected endpoints; routers call those functions to handle HTTP requests.

Environment
-----------
The application expects environment variables loaded from a .env file or the environment:

- DATABASE_URL — SQLAlchemy database URL (example for SQLite: sqlite:///./test.db, or a Postgres URL like postgresql://user:pass@host:5432/dbname)
- SECRET_KEY - unique secret key that only server knows
- ALGORITHM - the algorithm that will encode the token
- ACCESS_TOKEN_EXPIRE_MINUTES - the minutes that hold the token as verified 

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

API
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
  - Body: TodoUpdate (title, description, completed)
  - Updates the todo (only allowed for owner).
- DELETE /todos/{id}
  - Deletes the todo (only allowed for owner).


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
  - TodoUpdate: title, description, completed
  - TodoResponse: id, title, description, completed
