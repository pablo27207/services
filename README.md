# OOGSJ - Sistema de Observación

Este sistema forma parte del Observatorio Oceanográfico Golfo San Jorge (OOGSJ) y permite:

- Visualizar datos en tiempo real de plataformas oceanográficas, meteorológicas y mareógrafos.
- Integrar sensores remotos a través de APIs externas (como WeatherLink).
- Mostrar gráficas interactivas y mapas georreferenciados con Leaflet y D3.js.
- Administrar múltiples plataformas, variables sensadas y usuarios técnicos.
- Servir el frontend como una app estática con SvelteKit y el backend con Flask + PostgreSQL.

La arquitectura está basada en contenedores Docker con Nginx como proxy inverso, habilitado para HTTPS.

---

🛰️ Desarrollado para monitoreo ambiental y análisis científico en la región del Golfo San Jorge.
