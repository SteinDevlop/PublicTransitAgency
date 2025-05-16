FROM python:3.13

# Create a non-root user (e.g., "appuser")
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt . 
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY src/backend/app/ /app/

# Set appropriate permissions for the appuser to access the app directory
RUN chown -R appuser:appuser /app

# Change to the non-root user
USER appuser

# Expose the port that the app uses
EXPOSE 8000

# Command to start the application
CMD ["sh", "-c", "export PYTHONPATH=/src && fastapi dev .\\src\\backend\\app\\api\\main.py"]