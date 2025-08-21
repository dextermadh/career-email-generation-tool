# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for Streamlit, PyPDF2, Selenium, etc.)
RUN apt-get update && apt-get install -y \
    curl \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching layers)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variable to avoid prompts
ENV PYTHONUNBUFFERED=1

# Run Streamlit when container starts
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
