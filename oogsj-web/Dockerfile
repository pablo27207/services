# Etapa 1: Build con Node
FROM node:18 AS builder
WORKDIR /app

# Copiar dependencias primero para aprovechar la cache
COPY package*.json ./
RUN npm install

# Copiar el resto del proyecto
COPY . .

# Compilar el frontend como sitio estático (SvelteKit + adapter-static)
ENV VITE_PUBLIC_BASE_URL=https://oogsj.gob.ar
RUN npm run build

# Etapa 2: Servir con Nginx
FROM nginx:alpine

# Copiar los archivos estáticos generados al root que Nginx sirve
COPY --from=builder /app/build /usr/share/nginx/html

# Copiar tu configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto 80 (estándar HTTP, más simple)
EXPOSE 80

# Comando para iniciar Nginx en modo foreground
CMD ["nginx", "-g", "daemon off;"]

