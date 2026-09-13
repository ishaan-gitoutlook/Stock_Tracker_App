# Multi-purpose Dockerfile for Stock Tracker App (FastAPI & Streamlit)
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose default ports: 8501 (Streamlit) and 8000 (FastAPI)
EXPOSE 8501 8000

# Default command: launch the Streamlit Web Dashboard
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
