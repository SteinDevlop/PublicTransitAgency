FROM python:3.13

# Instalar dependencias necesarias y driver ODBC MS SQL
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

# Crear usuario no root
RUN adduser --disabled-password --gecos '' appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar paquetes Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente completo, ajusta según tu estructura
COPY src/backend /app/backend

# Ajustar permisos para appuser
RUN chown -R appuser:appuser /app

# Cambiar a usuario no root
USER appuser

# Puerto expuesto por FastAPI
EXPOSE 8000

# Variable de entorno para PYTHONPATH
ENV PYTHONPATH=/app/

# Comando para iniciar la app (ajusta la ruta si es necesario)
CMD ["sh", "-c", "export PYTHONPATH=/app && uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8000 --reload"]