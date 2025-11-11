# 🎬 FastAPI Movie Catalogue

A simple **CRUD API** built with **FastAPI**, **SQLModel**, and **SQLite**.  
The API allows users to list, create, update, and delete movies in a local database.  

---

## 🧭 Project Overview

| Component | Description |
|------------|-------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) – high-performance Python web framework |
| **ORM Layer** | [SQLModel](https://sqlmodel.tiangolo.com/) – combines SQLAlchemy + Pydantic |
| **Database** | SQLite |
| **Environment Tool** | [`uv`](https://github.com/astral-sh/uv) – fast Python package & environment manager |
| **Testing** | [pytest](https://docs.pytest.org/) + FastAPI TestClient |
| **CLI Utility** | [Typer](https://typer.tiangolo.com/) – for database seeding and listing movies |

---

## 🚀 Run Locally

### 1️⃣ Create a virtual environment

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run uvicorn app.main:app --reload
```

## 🧩 Endpoints

| Method | Path | Description |
|--------|------|--------------|
| `GET` | `/movies` | Retrieve all movies |
| `POST` | `/movies` | Add a new movie |
| `PUT` | `/movies/{id}` | Update an existing movie |
| `DELETE` | `/movies/{id}` | Delete a movie |

Example `POST` request (using `curl`):

```bash
curl -X POST "http://127.0.0.1:8000/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8}'
```

## 🌱 Database Management Commands (Typer CLI)

Use the built-in **Typer CLI** to manage your local SQLite database.  
Run any of these commands with:

```bash
uv run python -m app.cli <command>
```

- 🎬 **`seed`** – Creates the tables (if needed) and inserts a few sample movies for quick testing

- 📜 **`list`** – Displays all movies currently stored in the database in a simple text format.

- 🧹 **`reset`** – Deletes all movies from the database while keeping the schema intact, letting you start from a clean slate.

These commands make it easy to populate, inspect, or clear your database during development without manually opening SQLite.

## 🧪 Tests

This project includes simple **pytest** tests to verify that the main API routes work as expected.  
The tests use **FastAPI’s** built-in `TestClient` to simulate real HTTP requests in memory — no server startup required.

Run all tests with:

```bash
uv run pytest -v
```

✅ **What’s tested:**
- `POST /movies` — verifies that a new movie can be created successfully  
- `GET /movies` — checks that the list of movies is returned correctly  

Each test sends real requests to the API and asserts that the response codes and data match expectations.  
You can view detailed results in the terminal after running the command.
