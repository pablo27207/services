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

