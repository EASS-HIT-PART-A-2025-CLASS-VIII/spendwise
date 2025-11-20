# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Install uv (Python project manager) and dependencies
RUN pip install uv && uv pip install --system -r requirements.txt

# Expose Streamlit’s default port
EXPOSE 8501

# Command to run Streamlit
CMD ["uv", "run", "streamlit", "run", "app/dashboard.py", "--server.address=0.0.0.0"]
