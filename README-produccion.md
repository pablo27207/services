# 📦 Despliegue Producción - OOGSJ

Este entorno está pensado para producción (servidor real con dominio y HTTPS).  
Evita usar este entorno en local. Usa `Developer-Franco` para pruebas.

---

## 🐳 Levantar contenedores en producción

```bash
docker compose -f docker-compose.yml up -d


---------------------------------------------------------------------------------------------
Certbot se ejecuta automáticamente desde el contenedor certbot.

Para forzar una renovación manual:
docker exec certbot certbot renew

Para testear si el certificado es válido:
curl -v https://oogsj.gob.ar



----------------------------------------------------
Comandos útiles

docker compose ps           # Ver qué está corriendo
docker logs nginx_proxy     # Ver errores de NGINX
docker exec nginx_proxy nginx -t   # Test de configuración
docker restart nginx_proxy  # Reiniciar NGINX tras cambios

----------------------------------------------------------------

 Recomendaciones

Nunca subas .env o certificados reales.

Usá .gitignore para proteger todo lo sensible.

Nunca hagas merge desde main sin revisar manualmente los cambios.

Solo modificar nginx.prod.conf si sabés lo que hacés.