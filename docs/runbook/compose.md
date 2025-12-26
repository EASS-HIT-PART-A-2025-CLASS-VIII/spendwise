# Compose Runbook

This document provides instructions for orchestrating the SpendWise services, verifying system health, and running the automated validation suite.

## 1. Launching the Stack

The entire ecosystem is containerized and orchestrated via Docker Compose.

### Deployment
To build and start all services (Backend, Frontend, Worker, and Redis) in detached mode:
```bash
docker compose up -d --build
```


### Service Map
* **API (Backend)**: [http://localhost:8000](http://localhost:8000)
* **Interface (Frontend)**: [http://localhost:5173](http://localhost:5173)
* **Redis**: `localhost:6379`

---

## 2. Health & Telemetry Verification

### Container Status
Verify that all four cooperating services are healthy:
```bash
docker compose ps
```


### Backend Health Check
Confirm the FastAPI backend is responding to requests:
```bash
curl -I http://localhost:8000/auth/token
```


### Worker Logs
The AI Advisory worker processes reports asynchronously. Monitor its activity to verify background job ingestion:
```bash
docker compose logs -f worker
```


---

## 3. Rate-Limit Verification

The backend implements security guardrails including rate limiting. To verify health and rate-limit headers:
1.  Perform a request to a protected or public endpoint.
2.  Inspect the headers for `X-RateLimit` keys:
```bash
curl -I http://localhost:8000/transactions
```


---

## 4. Automated Validation (CI Simulation)

To ensure the local product is "tidy" and meets service contracts, run the following validation tools within the container environment.

### Pytest Suite
Runs all logic, security, and idempotency tests:
```bash
docker compose exec backend pytest
```


### Schemathesis (API Contract Testing)
Verifies that the API implementation matches the OpenAPI specification:
```bash
docker compose run --rm backend schemathesis run http://backend:8000/openapi.json
```


---

