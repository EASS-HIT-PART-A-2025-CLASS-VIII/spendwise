# 🧠 SpendWise Intelligence

Financial telemetry and AI-driven analysis backend powered by **FastAPI**, **SQLModel**, and **Redis**.

---

## 🚀 Execution

### Docker Compose

```bash
docker compose up --build
```

---

## 🧪 Testing

Run the containers and
execute the test suite within the container:

```bash
docker compose exec backend python -m pytest -v
```

---

## 🔐 Key Features

- **AI Neural Advisor:** Integrated LLM logic providing executive financial summaries and trend analysis.

- **Asynchronous Reporting:** Background PDF generation offloaded to dedicated workers via Redis to ensure zero API latency.

- **Financial Telemetry:** High-precision tracking and categorization of global transaction data.

- **Identity Management:** Secure, stateless JWT-based authentication with Bcrypt password hashing.

## 🛠 Tech Stack

- FastAPI (Web Framework)
- SQLModel (ORM & Models)
- Redis (Task Queue)
- Pytest (Validation)
- JWT (Security)
- React (Frontend)
- Typescript (Frontend Language)
- Docker (Containerization)
- Docker Compose (Orchestration)
