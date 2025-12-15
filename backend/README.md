# 🎬 FastAPI Movie API

A lightweight **CRUD backend** built with **FastAPI**, **SQLModel**, and **SQLite**.  
It provides endpoints to create, list, update, and delete movies, either locally or in a Docker container.

---

## 🚀 Quick Start

### Run locally
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run uvicorn app.main:app --reload
```

### Run with Docker
```bash
docker build -t fastapi-movies .
docker run --name fastapi-movies-container -p 8000:8000 fastapi-movies
```

📍 Visit → [http://localhost:8000/movies](http://localhost:8000/movies)

---

## 🧩 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/movies` | Get all movies |
| `POST` | `/movies` | Add a new movie |
| `PUT` | `/movies/{id}` | Update an existing movie |
| `DELETE` | `/movies/{id}` | Delete a movie |

Example:
```bash
curl -X POST "http://127.0.0.1:8000/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8}'
```

---

## 🌱 CLI Commands

Manage the database via Typer CLI:
```bash
uv run python -m app.cli <command>
```

| Command | Description |
|----------|-------------|
| `seed` | Seed DB from `data/movies.csv` |
| `list` | Display all movies |
| `reset` | Clear all movies from DB |

---

## 🧪 Tests

Run the tests:
```bash
uv run pytest -v
```

✅ Covers:  
- Create (`POST /movies`)  
- Read (`GET /movies`)  
- Update (`PUT /movies/{id}`)  
- Delete (`DELETE /movies/{id}`)

---

## 🧠 Tech Stack

- **FastAPI** – Web framework  
- **SQLModel** – ORM + Pydantic models  
- **Typer** – CLI utilities  
- **pytest** – Testing framework  
- **uv** – Dependency & environment manager
