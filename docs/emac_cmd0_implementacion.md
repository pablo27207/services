# Implementación: Estación EMAC CMD0 – Caleta Córdova

## Resumen

Se incorporó al sistema la estación hidrometeorológica **CMD0** del sistema EMAC/CRIBA, ubicada en Caleta Córdova. Mide seis variables combinadas (agua + atmósfera + viento) y publica sus datos a través de la misma API HTTP/CSV que la boya oceanográfica CIDMAR-2 ya existente.

| Dato | Valor |
|------|-------|
| Código de estación | `CMD0` |
| Coordenadas | -45.749189 lat, -67.368762 lon |
| Fuente de datos | http://emac.criba.edu.ar/servicios/ |
| Plataforma en BD | `Estación EMAC - Caleta Córdova CMD0` |
| Tipo de plataforma | Estación Meteorológica (id=4) |

---

## Archivos creados / modificados

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `db_init/migrations/20260601_add_emac_cmd0_station.sql` | Nuevo | Migración SQL con todas las entidades de BD |
| `api_ingestor/services/emac_cmd0_scraper.py` | Nuevo | Scraper de datos históricos CMD0 |
| `api_ingestor/services/task_config.py` | Modificado | Registro de la tarea Celery |

---

## 1. Migración de base de datos

### Por qué una migración separada

El proyecto ya tiene el patrón de un `init.sql` (estado inicial) más archivos en `db_init/migrations/` para cambios incrementales. Seguimos ese patrón para no tocar el `init.sql` original y garantizar que la migración se puede aplicar sobre una BD en producción sin reinicializarla.

### Qué hace la migración

```
20260601_add_emac_cmd0_station.sql
```

**Paso 1 – Nuevas variables** (tabla `oogsj_data.variable`):

| Variable nueva | Motivo |
|----------------|--------|
| `Nivel del Agua` | Distinto de `Nivel del Mar`; aquí es nivel local del cuerpo de agua |
| `Temperatura del Agua` | Temperatura del agua medida por sensor sumergido |
| `Conductividad del Agua` | Refleja salinidad/mineralización; no existía en el sistema |
| `Dirección del Viento` | Dirección puntual del viento (no el máximo ni el predominante) |

Las variables `Temperatura Exterior` y `Velocidad del Viento` ya existían y se reutilizan.

**Paso 2 – Nueva unidad**: `mS/cm` (miliSiemens por centímetro) para conductividad.

**Paso 3 – Nueva plataforma**: `Estación EMAC - Caleta Córdova CMD0`, tipo `Estación Meteorológica`.

**Paso 4 – Ubicación**: entrada en `platform_location_history` con las coordenadas exactas. `end_time = NULL` indica que es la posición actualmente vigente.

**Paso 5 – Seis sensores**:

| Sensor | var_code EMAC | Variable | Unidad BD | Conversión |
|--------|---------------|----------|-----------|-----------|
| Sensor de Nivel del Agua - CMD0 | 16 | Nivel del Agua | m | ninguna |
| Sensor de Temperatura del Agua - CMD0 | 13 | Temperatura del Agua | °C | ninguna |
| Sensor de Conductividad - CMD0 | 17 | Conductividad del Agua | mS/cm | ninguna |
| Sensor de Temperatura del Aire - CMD0 | 05 | Temperatura Exterior | °C | ninguna |
| Sensor de Velocidad del Viento - CMD0 | 03 | Velocidad del Viento | m/s | ÷ 3.6 (km/h → m/s) |
| Sensor de Dirección del Viento - CMD0 | 02 | Dirección del Viento | ° | ninguna |

### Idempotencia

Todos los `INSERT` usan `ON CONFLICT ... DO NOTHING` o cláusulas `WHERE NOT EXISTS`. La migración se puede aplicar múltiples veces sin crear duplicados ni errores.

### Cómo aplicar la migración

```bash
# Dentro del contenedor db (PostgreSQL):
docker exec -i services-db-1 psql -U postgres -d mis_datos \
  < db_init/migrations/20260601_add_emac_cmd0_station.sql

# O desde el host si PostgreSQL está expuesto:
psql -h localhost -U postgres -d mis_datos \
  -f db_init/migrations/20260601_add_emac_cmd0_station.sql
```

### Verificar que los sensores se crearon

```sql
SELECT s.id, s.name, v.name AS variable, u.symbol AS unidad
FROM   oogsj_data.sensor s
JOIN   oogsj_data.variable v ON v.id = s.variable_id
JOIN   oogsj_data.unit     u ON u.id = s.unit_id
WHERE  s.platform_id = (
           SELECT id FROM oogsj_data.platform
           WHERE name = 'Estación EMAC - Caleta Córdova CMD0'
       )
ORDER BY s.id;
```

Salida esperada (IDs reales pueden variar si hay insercciones previas fuera del init.sql):

```
 id |             name                          |        variable         | unidad
----+-------------------------------------------+-------------------------+-------
 78 | Sensor de Nivel del Agua - CMD0           | Nivel del Agua          | m
 79 | Sensor de Temperatura del Agua - CMD0     | Temperatura del Agua    | °C
 80 | Sensor de Conductividad - CMD0            | Conductividad del Agua  | mS/cm
 81 | Sensor de Temperatura del Aire - CMD0     | Temperatura Exterior    | °C
 82 | Sensor de Velocidad del Viento - CMD0     | Velocidad del Viento    | m/s
 83 | Sensor de Dirección del Viento - CMD0     | Dirección del Viento    | °
```

> **Importante**: si los `id` reales difieren de 78-83, actualizar el diccionario `VARIABLES` en `emac_cmd0_scraper.py` con los IDs correctos.

---

## 2. Scraper `emac_cmd0_scraper.py`

### Diseño

Sigue el mismo patrón que `buoy_scraper.py` (que también consulta la API EMAC/CRIBA):

```
EMACCMD0Scraper.fetch_station_data()
   ↓
   for cada var_code en VARIABLES:
       GET http://emac.criba.edu.ar/servicios/getHistoryValues.php
           ?station_code=CMD0&var_code=<XX>
       ↓
       parsea CSV (pandas)
       ↓
       aplica conversión de unidades si corresponde
       ↓
       acumula tuplas (timestamp, value, qf, pl_id, sensor_id, location_id)
   ↓
   retorna lista de tuplas
```

### Formato de respuesta de la API EMAC

El endpoint `getHistoryValues.php` devuelve un CSV con dos columnas:
- Columna 0: timestamp (formato ISO o similar)
- Columna 1: valor numérico

Ejemplo:
```
fecha,valor
2026-05-01 00:00:00,0.42
2026-05-01 01:00:00,0.45
...
```

### Conversión de unidades

Solo la velocidad del viento requiere conversión:

```python
# var_code="03": la API entrega km/h, almacenamos m/s
value_ms = value_kmh / 3.6
```

Las demás variables ya vienen en las unidades correctas (m, °C, mS/cm, °).

### Manejo de errores

El scraper no lanza excepciones hacia afuera. Cada variable se procesa independientemente. Si una falla (timeout, HTTP error, CSV mal formado), se logea el error y se continúa con la siguiente. Esto evita que un sensor con problemas bloquee la ingesta de los otros cinco.

```
[CMD0][OK]              → datos obtenidos y procesados correctamente
[CMD0][WARN]            → respuesta vacía o sin datos válidos
[CMD0][ERROR HTTP]      → timeout o código HTTP de error
[CMD0][ERROR RED]       → problema de red/DNS
[CMD0][ERROR DATOS]     → CSV mal formado
[CMD0][ERROR INESPERADO]→ cualquier otra excepción
```

### Tupla de retorno

Cada elemento de la lista retornada es:

```python
(timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)
# (datetime,  float, int,          int,                  int,       int        )
```

Este formato es el mismo que consumen `DBHandler.insert_measurements()` y todos los scrapers existentes.

---

## 3. Tarea Celery (`task_config.py`)

```python
"emac_cmd0_station": {
    "scraper":  EMACCMD0Scraper.fetch_station_data,
    "schedule": crontab(minute="*/30"),  # cada 30 minutos
},
```

### Por qué cada 30 minutos

- La boya y el mareógrafo se consultan cada 60/10 minutos respectivamente.
- La API EMAC entrega el **histórico de 30 días**; consultar con más frecuencia no provee nuevos datos históricos pero sí captura los puntos más recientes (la estación reporta con resolución sub-horaria en algunas variables).
- El constraint `UNIQUE (sensor_id, timestamp)` en la tabla `measurement` con `ON CONFLICT DO NOTHING` garantiza que los datos ya insertados no se duplican aunque el scraper los descargue de nuevo.
- 30 minutos es un compromiso razonable entre frescura y carga sobre el servidor EMAC.

---

## 4. Flujo de datos end-to-end

```
[Celery Beat]  cada 30 min
      ↓
[Celery Worker] ejecuta fetch_emac_cmd0_station
      ↓
[EMACCMD0Scraper.fetch_station_data()]
      ↓  HTTP GET × 6 variables
[API EMAC/CRIBA]
      ↓  respuesta CSV
[parse + conversión km/h→m/s]
      ↓  lista de tuplas
[DBHandler.insert_measurements()]
      ↓  INSERT ... ON CONFLICT DO NOTHING
[PostgreSQL: oogsj_data.measurement]
```

---

## 5. Notas adicionales

### Endpoint "último registro completo"

La API también expone:
```
http://emac.criba.edu.ar/servicios/getLastValues.php?station_code=CMD0
```

Este endpoint no se usa en el scraper actual porque el histórico de 30 días ya incluye el último valor. Si en el futuro se quiere un scraper de "solo el último punto" (más liviano, para alta frecuencia), basta con agregar un método adicional en `EMACCMD0Scraper` que consuma ese endpoint.

### Calidad de datos

Los datos se insertan con `quality_flag = 1` ("Bueno"), asumiendo que el sistema EMAC ya aplica un control de calidad básico en el sensor. Si en el futuro se desea aplicar QC propio (rango, outliers, etc.), el processing_level_id debería cambiar a 2 ("QC-1") o 3 ("QC-2").

### Zona horaria

La API EMAC devuelve timestamps sin información de zona horaria explícita. Se asume que están en **hora local argentina (UTC-3)**. `pandas.to_datetime` los parsea como naive datetime; si la tabla de mediciones requiere UTC, se deberá agregar una conversión:
```python
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize("America/Argentina/Buenos_Aires").dt.tz_convert("UTC")
```
Esto se puede validar comparando con los datos de la boya CIDMAR-2 (mismo sistema EMAC, misma estación).
