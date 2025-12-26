# EX3 Project Notes: SpendWise AI Financial Suite

This document details the architecture, security, and orchestration of the SpendWise platform, fulfilling the requirements for EX1, EX2, and EX3.

---

## 1. Project Overview
SpendWise is an integrated financial ecosystem providing real-time telemetry and intelligent advisory. It transitions from a FastAPI backend (EX1) and Vite interface (EX2) into a microservices architecture (EX3). The system enables users to track transactions and trigger asynchronous, AI-driven financial health analysis.

## 2. Service Architecture & Orchestration
The environment is orchestrated using Docker Compose across four dedicated services:

| Service | Role | Key Technologies |
| :--- | :--- | :--- |
| **Backend** | API Logic & Persistence | FastAPI, SQLModel |
| **Frontend** | User Dashboard | Vite, React |
| **Worker** | Async AI Analysis | Python, Arq |
| **Redis** | Telemetry & Task Queue | Redis 7 |

### Persistence & Data Consistency
Persistence is handled via **SQLite** using a shared Docker volume. The volume maps `./backend/app/data` on the host to `/app/app/data` inside the containers. This architecture ensures that the `backend` and `worker` services interact with the same `database.db` file concurrently.

---

## 3. Async Refresher & Telemetry (Session 09)
The system includes an async refresher logic to handle bulk data updates.

### Idempotency Logic
To prevent redundant processing, the system utilizes Redis-backed locks. Before starting an analysis, the service checks for an existing lock.

### Redis Telemetry Trace Excerpt
The following trace represents a successful task ingestion in the microservice stack:
```text
[REDIS] RPUSH arq:job_queue '{"job_id": "monthly_report_1", "function": "generate_monthly_report", "kwargs": {"user_id": 1}}'
[BACKEND] !!! JOB ENQUEUED FOR USER 1 !!!
[WORKER] Found job monthly_report_1. Starting execution...
[WORKER] Job monthly_report_1 completed.
```


---

## 4. Security Baseline (Session 11)
The project implements a layered security model:
* **Credential Protection**: Passwords are encrypted using Bcrypt hashing before storage.
* **Authentication**: Stateless authentication is handled via JWT tokens.
* **Route Protection**: Critical financial endpoints require a valid `Authorization: Bearer <token>` header.

### Secret Rotation Procedure
1.  Generate a secure 32-byte hex string.
2.  Update the `JWT_SECRET_KEY` in the `.env` file.
3.  Restart services using `docker compose up -d`.
4.  Existing tokens are immediately invalidated, forcing re-authentication across the stack.

---

## 5. AI Integration Enhancement
The core EX3 enhancement is the **AI Financial Advisory Worker**.
* **Mechanism**: The backend enqueues a `generate_monthly_report` job into Redis.
* **Worker Role**: The `worker` service pulls the job, analyzes transaction patterns, and generates a personalized report stored in the `app/data/reports` directory.
* **Access**: Reports are served statically via the `/reports-files` endpoint.

---

## 6. AI Assistance Section
**Tools Used**: Gemini (Google).

**Prompts Provided**:
* Determining optimal database location for containerized SQLite.
* Resolving `NoReferencedTableError` by registering models in the metadata registry.
* Drafting an async refresher with Redis-backed idempotency and bounded concurrency.
* Updating test suites to use `ASGITransport` for modern `httpx` compatibility.

**Verification**:
* System orchestration was verified using the `scripts/demo.sh` script.
* Database persistence was confirmed by verifying the integrity of `database.db` across container restarts.
* Security constraints were validated via automated tests ensuring `401 Unauthorized` responses for missing tokens.

---

## 7. Setup & Local Demo
The project uses a self-healing CLI to automate setup. Running the seed command automatically initializes tables and creates a default user if none exist.

**Automated Setup**:
```bash
./backend/scripts/demo.sh
```