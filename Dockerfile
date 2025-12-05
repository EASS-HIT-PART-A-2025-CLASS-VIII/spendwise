FROM python:3.12-slim

WORKDIR /app

COPY . .

# ---- Install uv, create venv and install requirements ----
RUN pip install --no-cache-dir uv && \
    uv venv && \
    uv pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# ---- Start FastAPI app using uv ----
CMD ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]