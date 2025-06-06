# Etapa 1: Construcción
FROM python:3.9-slim AS builder
WORKDIR /app

# 🔧 ESTA PARTE ES FUNDAMENTAL: sin esto pandas falla
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers=2", "--access-logfile=-", "app:app"]
