FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]