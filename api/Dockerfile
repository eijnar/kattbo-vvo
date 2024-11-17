FROM python:3.11-slim

# Create appuser
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install gosu
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends gosu; \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app/api

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership of application files
RUN chown -R appuser:appuser /app

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT [ "/entrypoint.sh" ]

# Start the application, currently using uvicorn
CMD ["uvicorn", "main:create_app", "--uds", "./kattbo-vvo-api-uvicorn.sock", "--factory"]