FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Default command (production mode)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
