FROM python:3.13

# Update and install required packages and ODBC driver
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    lsb-release \
    gnupg \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend files to maintain the existing structure
COPY src/backend /app/backend

# Copy frontend files to a separate directory
COPY src/frontend /app/frontend

# Set ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Set environment variable for Python path
ENV PYTHONPATH=/app/

# Start the FastAPI application with the same command
CMD ["sh", "-c", "export PYTHONPATH=/app && uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8000 --reload --lifespan on"]
