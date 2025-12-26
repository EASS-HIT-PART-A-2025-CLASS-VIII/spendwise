# 🧠 SpendWise Intelligence
AI-driven financial analysis platform built with a Vite-based frontend and a robust FastAPI backend, utilizing Redis for real-time telemetry and SQLModel for efficient data management.
---

## 🚀 Execution

### Docker Compose

- make sure to create a .env in the project root with the necessary environment variables as specified in the .env.example file.

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
## 🛠️ Database Management (CLI)

SpendWise includes a powerful Command Line Interface to manage your financial telemetry. You can execute these commands directly within the `backend` container.

#### **Commands**

* **Seed**: Populates the database with 50 sample transactions from a CSV file, these transactions are set for the first user registered.
  ```bash
  docker compose exec backend python -m app.cli seed
  ```
* **List**: Displays all financial logs currently stored in your ledger.
  ```bash
  docker compose exec backend python -m app.cli list-transactions
  ```
* **Reset**: Wipes all transaction data while preserving the database schema.
  ```bash
  docker compose exec backend python -m app.cli reset
  ```

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
