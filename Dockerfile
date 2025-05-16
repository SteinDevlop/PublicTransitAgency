# Utiliza una imagen base de Python
FROM python:3.13

# Crear un usuario no root
RUN adduser --disabled-password --gecos '' appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al directorio de trabajo
COPY src/backend/app/ /app/

# Establecer el PYTHONPATH para el entorno de FastAPI
ENV PYTHONPATH=/app

# Asignar permisos al usuario
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]