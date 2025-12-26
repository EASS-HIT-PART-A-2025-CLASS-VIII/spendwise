#!/bin/bash

echo "--- 🛠 SpendWise EX3 Demo ---"

echo "1. Starting stack..."
docker compose up -d --build

echo "2. Waiting for services to stabilize..."
sleep 10

echo "3. Seeding Database (Auto-creates Tables & User)..."
docker compose exec backend python -m app.cli seed

echo "4. Running Async Refresher (Inside Container)..."
docker compose exec backend python -m scripts.refresh

echo "5. Running Automated Tests..."
docker compose exec backend pytest

echo "--- ✅ Demo Complete ---"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"