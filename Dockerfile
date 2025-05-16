# Imagen base de Python
FROM python:3.13

# Crear un usuario no root
RUN adduser --disabled-password --gecos '' appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todo el código desde src
COPY src/ /app/src/

# Ajustar el PYTHONPATH para que FastAPI encuentre el módulo backend
ENV PYTHONPATH=/app/src

# Asignar permisos al usuario
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Exponer el puerto que utiliza la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "backend.app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]