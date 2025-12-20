FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]