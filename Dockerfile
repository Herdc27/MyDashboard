# --- Etapa1:Builder ---
FROM python:3.11-slim  as builder

# Evita que python genere archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNDUFFERED=1

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalamos las dependecias 
COPY requeriments.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requeriments.txt
# -- Etapa 2: Final (Imagen produccion) --
FROM python:3.11-slim

# Creamos el usuario no-root por seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
# Copiamos el archivo .env para las variables de entorno

# Compiamos los wheels compilamos de la etapa anterior
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requeriments.txt .

# Instalamos las dependencias desde los wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requeriments.txt

# Copiamos el codigo de la aplicacion
COPY ./MyDasboard/src .

# CAmbiamos elususariosin privilegios
USER appuser

# Expomenos el puerto
EXPOSE 5000

# Set Flask app for migrations
ENV FLASK_APP=wsgi.py

# Comando de arranque: run migrations then start Gunicorn
CMD ["sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:5000 wsgi:application"]

