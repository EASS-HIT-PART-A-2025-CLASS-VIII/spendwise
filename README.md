# 🧠 SpendWise Intelligence

Full-stack financial intelligence: A multi-service ecosystem (EX1–EX3) powered by FastAPI, Vite, SQLModel, and Redis, featuring AI-driven insights and orchestrated via Docker Compose.


---

## 🚀 Execution

### Docker Compose

- make sure to create a .env in the project root with the necessary environment variables as specified in the .env.example file.
- VITE_API_URL should be http://localhost:8000

```bash
docker compose up --build
```

- After successfully running the containers the UI will be accessible at http://localhost:5173
- Now register a user via the UI to get started.
- recommended to seed the database now according to the instructions below.

---

## 🛠️ Database Management (CLI)

SpendWise includes a powerful Command Line Interface to manage your financial telemetry. You can execute these commands directly within the `backend` container.

#### **Commands**

* **Seed**: Populates the database with 50 sample transactions from a CSV file, these transactions are set for the first user registered, make sure to register a user before running this.
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
---

## 🧪 Testing
The project includes a comprehensive test suite covering core logic, security, and microservice service contracts.

### Running Tests
Execute the full suite inside the backend container environment:
```bash
docker compose exec backend pytest -v
```
### Test Categories
* **Core Transactions (`tests/test_transactions.py`):** Verifies the EX1/EX2 CRUD logic, including user registration, transaction creation, and dashboard statistics.
* **Security Baseline (`tests/test_security.py`):** Ensures JWT protection is active, verifying that missing tokens or malformed credentials result in `401 Unauthorized` responses.
* **Async & Idempotency (`tests/test_refresh.py`):** Validates the microservice service contract by ensuring Redis locks prevent redundant AI analysis tasks.

### Local Demo
To see the entire lifecycle (Build -> Seed -> Refresh -> Test), run:
```bash
./backend/scripts/demo.sh
```

---
## 🤖 AI Assistance
This project utilized **Gemini (Google)** to assist in the following areas:
* **Architecture Design:** Guided the transition from a monolithic backend to a containerized microservices stack using Docker Compose and Redis.
* **Debugging:** Assisted in resolving `NoReferencedTableError` during database seeding by identifying missing model imports in the CLI metadata registry.
* **Async Logic:** Developed the `refresh.py` utility using `asyncio.Semaphore` for bounded concurrency and Redis for idempotency logic.
* **Security Baseline:** Helped implement JWT role-based access control and modern `httpx.ASGITransport` testing syntax for the security suite.
* **Verification:** All AI-generated code snippets were manually verified by running the `demo.sh` orchestration script and ensuring 100% test coverage in the local Docker environment.
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
