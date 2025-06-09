# Etapa 1: Build con Node
FROM node:18 AS builder
WORKDIR /app

# Copiar dependencias primero para mejor cache
COPY package*.json ./
RUN npm install

# Copiar el resto del proyecto
COPY . .

# 🧠 Acá se define la URL del dominio personalizado
ENV VITE_PUBLIC_BASE_URL=http://proyectosdesarrollo.com.ar

# Compilar el frontend con esa URL
RUN npm run build

# Etapa 2: Servir con Nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 81
CMD ["nginx", "-g", "daemon off;"]

