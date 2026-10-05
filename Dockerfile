# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data \
    PORT=5000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create volume mount directory for SQLite persistent database
RUN mkdir -p /app/data

# Define persistent Docker volume
VOLUME ["/app/data"]

# Expose container port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
