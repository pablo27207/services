# Etapa 1: Construcción
FROM python:3.9-slim AS builder
WORKDIR /app

COPY requirements.txt .  
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /install /usr/local  
COPY . .  

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers=2", "--access-logfile=-", "app:app"]

