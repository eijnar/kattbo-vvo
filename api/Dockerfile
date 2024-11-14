FROM python:3.11-slim

# Create appuser
RUN groupadd -r appuser && useradd -r -g appuser appuser

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
ENTRYPOINT [ "/entrypoint.sh" ]

# Start the application, currently using uvicorn
CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000"]