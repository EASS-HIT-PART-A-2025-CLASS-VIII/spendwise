# ---- Base image ----
FROM python:3.12-slim

# ---- Set workdir ----
WORKDIR /app

# ---- Copy project files ----
# ---- Copy project files ----
COPY . .

# ---- Install uv and project dependencies ----
RUN pip install --no-cache-dir uv && \
    uv venv && \
    uv pip install --no-cache-dir -r requirements.txt

# ---- Expose FastAPI port ----
EXPOSE 8000

# ---- Start FastAPI app using uv ----
CMD ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
