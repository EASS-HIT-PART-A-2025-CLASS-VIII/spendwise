FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# ---- Install uv, create venv and install requirements ----
RUN pip install --no-cache-dir uv && \
    uv venv && \
    uv pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]