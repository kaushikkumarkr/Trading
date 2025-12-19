# Base Python Image (Slim for speed)
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Install System Dependencies (Git is needed for some pip installs)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy Requirements
COPY requirements.txt .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Set Env Vars (Can be overridden by Docker/K8s)
ENV PYTHONUNBUFFERED=1

# Default Command (Run the Loop)
CMD ["python", "-u", "-m", "trading_system.main"]
