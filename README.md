# FastAPI Starter Template

🚀 Ready-to-use FastAPI starter template featuring built-in user authentication, secure database configuration, and a clean modular architecture. Jumpstart your backend development!

## Features

- **User authentication**: registration, login and token refresh
- **JWT in HttpOnly cookies** (access + refresh tokens) powered by [AuthX](https://github.com/yezz123/authx)
- **Secure password hashing** with [pwdlib](https://github.com/frankie567/pwdlib) (recommended algorithm)
- **SQLAlchemy ORM** with automatic table creation on startup
- **Environment-based configuration** via `.env` (secrets never live in the code)
- **Clean modular structure**: core, auth and users are separated
- **Database health check** endpoint
- **CORS middleware** ready for a separate frontend

## Tech Stack

| Component      | Library          |
| -------------- | ---------------- |
| Web framework  | FastAPI          |
| ORM            | SQLAlchemy       |
| Auth / JWT     | AuthX            |
| Password hash  | pwdlib           |
| Config         | python-dotenv    |
| Server         | Uvicorn          |

## Project Structure

```
.
├── app
│   ├── main.py                 # App entry point, middleware, routers
│   ├── core
│   │   ├── config.py           # Env variables, AuthX configuration
│   │   ├── database.py         # Engine, session, Base, DB health check
│   │   └── security.py         # Auth cookie helpers
│   └── models
│       ├── auth
│       │   ├── api.py          # /register, /login, /refresh
│       │   ├── schemas.py      # Pydantic schemas
│       │   └── services.py     # Auth business logic
│       └── users
│           ├── api.py          # User endpoints
│           ├── models.py       # User ORM model
│           └── schemas.py
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/VoidStrike404/fastapi_starting_folder.git
cd fastapi_starting_folder
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (see `.env.example`):

```env
JWT_SECRET_KEY=your_long_random_secret
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

Generate a strong secret key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

> `DATABASE_URL` can be any database supported by SQLAlchemy (make sure the matching driver is installed).

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint          | Description                                   |
| ------ | ----------------- | --------------------------------------------- |
| GET    | `/`               | Welcome message                               |
| GET    | `/check-db`       | Check the database connection                 |
| POST   | `/register`       | Register a new user                           |
| POST   | `/login`          | Log in and receive auth cookies               |
| POST   | `/refresh`        | Issue new tokens using the refresh cookie     |
| GET    | `/get_all_users`  | List users                                    |

### Example requests

**Register**

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "strong_password"}'
```

**Login** (saves cookies to a file)

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "john", "password": "strong_password"}'
```

**Refresh tokens**

```bash
curl -X POST http://127.0.0.1:8000/refresh -b cookies.txt -c cookies.txt
```

## How Authentication Works

1. The user registers; the password is hashed before being stored.
2. On login, the server creates an **access token** (15 minutes) and a **refresh token** (7 days).
3. Both tokens are set as **HttpOnly cookies** (`my_access_token`, `my_refresh_token`), so JavaScript cannot read them.
4. When the access token expires, the client calls `/refresh` to get a new pair.

## Before Going to Production

- [ ] Set `secure=True` for cookies in `app/core/security.py` and serve the app over HTTPS
- [ ] Replace `allow_origins=["*"]` in `app/main.py` with your real frontend origins
- [ ] Remove tokens from JSON response bodies (they are already in HttpOnly cookies)
- [ ] Protect or remove endpoints that expose user data, and never return password hashes
- [ ] Use a strong, unique `JWT_SECRET_KEY` and never commit `.env`
- [ ] Use migrations (e.g. Alembic) instead of `create_all` on startup

## Contributing

Contributions, issues and feature requests are welcome. Feel free to open an issue or submit a pull request.

## License

This project is open source. Add a license of your choice (for example, [MIT](https://choosealicense.com/licenses/mit/)).
