# 🧠 SpendWise Backend Intelligence

The core engine of the SpendWise platform, providing high-performance financial telemetry, AI-driven insights, and automated background reporting via **FastAPI**, **SQLModel**, and **Redis**.

---

## 🚀 Local Development Setup

To run the backend on your host machine without Docker, follow these steps to ensure a clean environment.

### 1. Prerequisites

- **Python 3.12+**
- **Redis** (Must be running locally for the worker and AI advice endpoints)
- **uv** (Highly recommended for fast dependency management)

### 2. Environment Setup

````bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt


### 3. Configuration
Create a `.env` file in the project root directory:

```env
JWT_SECRET_KEY=your_super_secret_key_here
OPEN_AI_API_KEY=your_openai_api_key_here
````

### 4. Running the API

```bash
uv run uvicorn app.main:app --reload
```

📍 Swagger Documentation: http://localhost:8000/docs

---

## ⚙️ Background Worker

SpendWise uses a worker to handle heavy tasks like PDF generation. In a local setup, you must run the worker in a separate terminal:

```bash
# Ensure venv is active
export PYTHONPATH=.
python -m app.worker
```

---

## 🧪 Testing Suite

We use **pytest** to validate the financial logic and security layers.

**Run tests locally:**

```bash
uv run pytest -v
```

**Run tests via Docker (if containers are up):**

```bash
docker compose exec backend python -m pytest -v
```

---

## 🏗 Backend Architecture

- **app/routes.py**: Route handlers for API endpoints.
- **app/services/**: Complex business logic (AI prompt engineering, calculation engines).
- **app/dals/**: Data Access Layer for clean database interactions.
- **app/models/**: SQLModel definitions for database schema and Pydantic validation.
- **app/core/**: Security, JWT logic, and global configurations.
- **app/worker.py**: Background task definitions for Redis.

---

## 🛠 Tech Stack

- **FastAPI**: Modern web framework.
- **SQLModel**: Combined SQLAlchemy and Pydantic power.
- **Redis**: High-speed message brokerage.
- **uv**: Ultra-fast Python package management.
- **Pytest**: Industry-standard test framework.
