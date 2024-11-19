FROM python:3.11-slim

# Create appuser
RUN groupadd -r appuser -g 2000 && useradd -r -u 2000 -g appuser appuser

# Install gosu
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends gosu; \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app/api

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
#ENTRYPOINT [ "/entrypoint.sh" ]

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]

# Start the application, currently using uvicorn
#CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--ssl-certfile", "/app/secrets/certfile.crt", "--ssl-keyfile", "/app/secrets/keyfile.key"]