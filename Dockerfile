# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install Python and required system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/

# Set environment variables
ENV PYTHONPATH=/app
ENV ALLOWED_ORIGINS=http://localhost:3001
ENV DEVICE=cuda

# Create necessary directories
RUN mkdir -p backend/uploads backend/results

# Expose port
EXPOSE 8000

# Run the application
CMD ["python3", "backend/app.py"]
