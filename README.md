# 🎬 FastAPI Movies Monorepo

A full-stack movie catalogue application built with FastAPI and Streamlit.
It provides a lightweight API backend for managing movies and a simple web dashboard for interacting with the data locally or in Docker.

## 🧭 Overview

| Component | Description |
|------------|-------------|
| **Backend** | FastAPI + SQLModel + SQLite – REST API for creating, reading, updating, and deleting movies |
| **Frontend** | Streamlit – interactive dashboard to browse, add, delete, and export movies |
| **Database** | Lightweight SQLite database stored locally at `backend/app/data/movies.db` |
| **Deployment** | Docker Compose configuration running backend and frontend as connected services |
| **Testing** | Pytest suite validating API endpoints and database logic |
| **CLI Tools** | Typer-based commands for database seeding, listing, and exporting movies |





## 🐳 Run with Docker Compose

To start both backend (FastAPI) and frontend (Streamlit) containers together:

```bash
docker compose up --build
```
Then open:

Backend → http://localhost:8000/movies

Frontend → http://localhost:8501

### 🧰 Common Commands
```bash

docker compose down             # Stop all running containers
docker compose ps               # List active containers
docker logs backend             # View FastAPI logs
docker logs frontend            # View Streamlit logs
```
## 🧩 Features

- List all movies in a table

- Add new movies (validated fields)

- Delete movies by ID

- Export movies to CSV

- Caching and refresh in Streamlit

- Fully functional inside Docker Compose

## 🧪 Testing

To run backend tests:

```bash
cd backend
uv run pytest -v
```

## 📚 Technologies

- FastAPI

- SQLModel

- Streamlit

- Typer

- Docker Compose

- pytest

- uv

### 🧠 Notes

- MOVIE_API_BASE_URL is automatically configured inside Docker Compose (http://backend:8000).

- The project intentionally stays small and local (no external DB or cloud hosting).
