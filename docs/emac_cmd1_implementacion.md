# Implementación: Estación EMAC CMD1

## Resumen

Se incorporó al sistema la estación hidrometeorológica **CMD1** del sistema EMAC/CRIBA. Mide seis variables combinadas (agua + atmósfera + viento) y publica sus datos a través de la misma API HTTP/CSV que CMD0.

| Dato | Valor |
|------|-------|
| Código de estación | `CMD1` |
| Coordenadas | -45.831766 lat, -67.462439 lon |
| Fuente de datos | http://emac.criba.edu.ar/servicios/ |
| Plataforma en BD | `Estación EMAC - CMD1` |
| Tipo de plataforma | Estación Meteorológica (id=4) |

---

## Archivos creados / modificados

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `db_init/migrations/20260701_add_emac_cmd1_station.sql` | Nuevo | Migración SQL con todas las entidades de BD |
| `api_ingestor/services/emac_cmd1_scraper.py` | Nuevo | Scraper de datos históricos CMD1 |
| `api_ingestor/services/task_config.py` | Modificado | Registro de la tarea Celery `emac_cmd1_station` |
| `web_app/blueprints/emac_cmd1_bp.py` | Nuevo | Endpoints REST + documentación Swagger |
| `web_app/app.py` | Modificado | Import y registro del blueprint, actualización del tag EMAC |

---

## 1. Migración de base de datos

### Qué hace la migración

```
20260701_add_emac_cmd1_station.sql
```

**Paso 1 – Variables**: usa `ON CONFLICT DO NOTHING` porque ya fueron creadas por CMD0. La migración es idempotente y segura de aplicar en cualquier orden.

**Paso 2 – Unidad**: `mS/cm` — igual que CMD0, idempotente.

**Paso 3 – Nueva plataforma**: `Estación EMAC - CMD1`, tipo `Estación Meteorológica`.

**Paso 4 – Ubicación**: coordenadas (-45.831766, -67.462439), `end_time = NULL`.

**Paso 5 – Seis sensores**:

| Sensor | var_code EMAC | Variable | Unidad BD | Conversión |
|--------|---------------|----------|-----------|-----------|
| Sensor de Nivel del Agua - CMD1 | 16 | Nivel del Agua | m | ninguna |
| Sensor de Temperatura del Agua - CMD1 | 13 | Temperatura del Agua | °C | ninguna |
| Sensor de Conductividad - CMD1 | 17 | Conductividad del Agua | mS/cm | ninguna |
| Sensor de Temperatura del Aire - CMD1 | 05 | Temperatura Exterior | °C | ninguna |
| Sensor de Velocidad del Viento - CMD1 | 03 | Velocidad del Viento | m/s | ÷ 3.6 (km/h → m/s) |
| Sensor de Dirección del Viento - CMD1 | 02 | Dirección del Viento | ° | ninguna |

### Cómo aplicar la migración

```bash
# Dentro del contenedor db (PostgreSQL):
docker exec -i services-db-1 psql -U postgres -d mis_datos \
  < db_init/migrations/20260701_add_emac_cmd1_station.sql

# O desde el host si PostgreSQL está expuesto:
psql -h localhost -U postgres -d mis_datos \
  -f db_init/migrations/20260701_add_emac_cmd1_station.sql
```

### Verificar que los sensores se crearon

```sql
SELECT s.id, s.name, v.name AS variable, u.symbol AS unidad
FROM   oogsj_data.sensor s
JOIN   oogsj_data.variable v ON v.id = s.variable_id
JOIN   oogsj_data.unit     u ON u.id = s.unit_id
WHERE  s.platform_id = (
           SELECT id FROM oogsj_data.platform
           WHERE name = 'Estación EMAC - CMD1'
       )
ORDER BY s.id;
```

---

## 2. Scraper `emac_cmd1_scraper.py`

Sigue exactamente el mismo patrón que `emac_cmd0_scraper.py`. Resuelve `sensor_id` y `location_id` dinámicamente desde la BD por nombre de plataforma.

```
EMACCMD1Scraper.fetch_station_data()
   ↓
   for cada var_code en variables resueltas:
       GET http://emac.criba.edu.ar/servicios/getHistoryValues.php
           ?station_code=CMD1&var_code=<XX>
       ↓
       parsea CSV (pandas)
       ↓
       aplica conversión km/h→m/s para velocidad del viento
       ↓
       acumula tuplas (timestamp, value, qf, pl_id, sensor_id, location_id)
   ↓
   retorna lista de tuplas
```

---

## 3. Tarea Celery (`task_config.py`)

```python
"emac_cmd1_station": {
    "scraper":  EMACCMD1Scraper.fetch_station_data,
    "schedule": crontab(minute="*/30"),  # cada 30 minutos
},
```

Mismo intervalo que CMD0 por las mismas razones (API entrega 30 días, constraint UNIQUE evita duplicados).

---

## 4. Endpoints REST (`emac_cmd1_bp.py`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/emac_cmd1/` | Último dato de cada variable |
| GET | `/api/emac_cmd1/history` | Serie temporal últimos 10 días |

Documentados con Swagger bajo el tag `EMAC`. Misma estructura de respuesta que CMD0.

---

## 5. Flujo de datos end-to-end

```
[Celery Beat]  cada 30 min
      ↓
[Celery Worker] ejecuta fetch_emac_cmd1_station
      ↓
[EMACCMD1Scraper.fetch_station_data()]
      ↓  HTTP GET × 6 variables
[API EMAC/CRIBA]
      ↓  respuesta CSV
[parse + conversión km/h→m/s]
      ↓  lista de tuplas
[DBHandler.insert_measurements()]
      ↓  INSERT ... ON CONFLICT DO NOTHING
[PostgreSQL: oogsj_data.measurement]
```
