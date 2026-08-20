FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (needed for some compiling, e.g., chromadb)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Start the FastAPI server using uvicorn
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
