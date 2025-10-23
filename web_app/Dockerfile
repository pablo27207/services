# Etapa 1: Construcción (Instalación de dependencias)
FROM python:3.9-slim AS builder
WORKDIR /install_deps

# Copiamos solo el archivo de dependencias para aprovechar el cache de Docker
COPY requirements.txt .  
RUN pip install --no-cache-dir --prefix=/usr/local -r requirements.txt

# Etapa 2: Imagen final (Entorno de ejecución)
FROM python:3.9-slim
WORKDIR /app

# Copiamos los paquetes instalados
COPY --from=builder /usr/local /usr/local

# Copiamos todo el código de la aplicación (incluyendo app.py, usuarios.py, etc.)
# Nota: El contexto de construcción es ./web_app
COPY . /app/  

# Comando de inicio de Gunicorn.
# app:app significa: busca el módulo 'app' (app.py) y usa la instancia 'app' (Flask app)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers=2", "--access-logfile=-", "app:app"]
