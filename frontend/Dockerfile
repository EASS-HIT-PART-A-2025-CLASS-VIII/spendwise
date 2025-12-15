FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv && uv pip install --system -r requirements.txt

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]
