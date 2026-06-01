-- =============================================================================
-- Migración: Estación EMAC CMD0 - Caleta Córdova
-- Fecha: 2026-06-01
-- Descripción: Agrega la plataforma, ubicación, variables, unidades y sensores
--              para la estación hidrometeorológica CMD0 del sistema EMAC/CRIBA
--              ubicada en Caleta Córdova (-45.749189, -67.368762).
--
-- Variables que incorpora:
--   var_code=16 → Nivel del Agua (m)
--   var_code=13 → Temperatura del Agua (°C)
--   var_code=17 → Conductividad (mS/cm)
--   var_code=05 → Temperatura del Aire (°C)
--   var_code=03 → Velocidad del Viento (km/h en API → almacenada como m/s)
--   var_code=02 → Dirección del Viento (°)
--
-- Cómo aplicar:
--   psql -U <user> -d <dbname> -f 20260601_add_emac_cmd0_station.sql
-- =============================================================================

BEGIN;

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. NUEVAS VARIABLES
--    ON CONFLICT (name) DO NOTHING → idempotente: si ya existe, no falla.
-- ─────────────────────────────────────────────────────────────────────────────

-- Nivel del Agua: distinto de "Nivel del Mar" (que es relativo al datum global).
-- Este sensor mide el nivel en el sitio de la estación (escala local).
INSERT INTO oogsj_data.variable (name, description)
VALUES ('Nivel del Agua', 'Nivel del agua en metros respecto al nivel de referencia local de la estación')
ON CONFLICT (name) DO NOTHING;

-- Temperatura del Agua: temperatura registrada por el sensor sumergido.
INSERT INTO oogsj_data.variable (name, description)
VALUES ('Temperatura del Agua', 'Temperatura del agua medida por sensor sumergido, en grados Celsius')
ON CONFLICT (name) DO NOTHING;

-- Conductividad del Agua: indica salinidad/mineralización del agua.
INSERT INTO oogsj_data.variable (name, description)
VALUES ('Conductividad del Agua', 'Conductividad eléctrica del agua en miliSiemens por centímetro; refleja la salinidad/mineralización')
ON CONFLICT (name) DO NOTHING;

-- Dirección del Viento: ángulo desde donde sopla el viento (0°=Norte, 90°=Este).
INSERT INTO oogsj_data.variable (name, description)
VALUES ('Dirección del Viento', 'Dirección desde la que sopla el viento, expresada en grados (0°=Norte, 90°=Este, etc.)')
ON CONFLICT (name) DO NOTHING;


-- ─────────────────────────────────────────────────────────────────────────────
-- 2. NUEVA UNIDAD: miliSiemens por centímetro (para conductividad)
--    ON CONFLICT (symbol) DO NOTHING → idempotente.
-- ─────────────────────────────────────────────────────────────────────────────

INSERT INTO oogsj_data.unit (name, symbol)
VALUES ('miliSiemens por centímetro', 'mS/cm')
ON CONFLICT (symbol) DO NOTHING;


-- ─────────────────────────────────────────────────────────────────────────────
-- 3. NUEVA PLATAFORMA
--    platform no tiene UNIQUE en name → usamos WHERE NOT EXISTS para idempotencia.
-- ─────────────────────────────────────────────────────────────────────────────

-- Tipo 4 = 'Estación Meteorológica' (definido en init.sql).
-- CMD0 es en realidad una estación hidrometeorológica (mide agua + aire + viento).
INSERT INTO oogsj_data.platform (name, platform_type_id)
SELECT
    'Estación EMAC - Caleta Córdova CMD0',
    pt.id
FROM oogsj_data.platform_type pt
WHERE pt.name = 'Estación Meteorológica'
  AND NOT EXISTS (
      SELECT 1
      FROM oogsj_data.platform
      WHERE name = 'Estación EMAC - Caleta Córdova CMD0'
  );


-- ─────────────────────────────────────────────────────────────────────────────
-- 4. UBICACIÓN DE LA PLATAFORMA
--    start_time = fecha aproximada de inicio de operaciones conocida.
--    end_time = NULL → ubicación actualmente vigente.
-- ─────────────────────────────────────────────────────────────────────────────

INSERT INTO oogsj_data.platform_location_history
    (platform_id, latitude, longitude, depth, start_time, end_time)
SELECT
    p.id,
    -45.749189,
    -67.368762,
    0,                          -- Sensor en superficie (nivel 0)
    '2025-01-01 00:00:00',
    NULL                        -- Ubicación vigente
FROM oogsj_data.platform p
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND NOT EXISTS (
      SELECT 1
      FROM oogsj_data.platform_location_history plh
      WHERE plh.platform_id = p.id
        AND plh.latitude   = -45.749189
        AND plh.longitude  = -67.368762
  );


-- ─────────────────────────────────────────────────────────────────────────────
-- 5. SENSORES DE LA PLATAFORMA CMD0
--    Cada INSERT es idempotente: solo inserta si no existe ese sensor
--    (mismo name + platform_id) para evitar duplicados en re-ejecución.
--
--    Orden de inserción → orden de IDs esperados (asumiendo DB limpia desde init.sql):
--      78: Nivel del Agua
--      79: Temperatura del Agua
--      80: Conductividad
--      81: Temperatura del Aire
--      82: Velocidad del Viento
--      83: Dirección del Viento
--
--    Nota: si la secuencia del sensor está en un valor distinto al esperado,
--    los IDs reales serán distintos. En ese caso actualizar VARIABLES en
--    emac_cmd0_scraper.py consultando:
--      SELECT id, name FROM oogsj_data.sensor WHERE platform_id = <id_plataforma>;
-- ─────────────────────────────────────────────────────────────────────────────

-- Sensor: Nivel del Agua (var_code=16) → metros (m)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Nivel del Agua - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Nivel del Agua'
  AND u.symbol = 'm'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Nivel del Agua - CMD0' AND platform_id = p.id
  );

-- Sensor: Temperatura del Agua (var_code=13) → grados Celsius (°C)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Temperatura del Agua - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Temperatura del Agua'
  AND u.symbol = '°C'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Temperatura del Agua - CMD0' AND platform_id = p.id
  );

-- Sensor: Conductividad (var_code=17) → miliSiemens por centímetro (mS/cm)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Conductividad - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Conductividad del Agua'
  AND u.symbol = 'mS/cm'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Conductividad - CMD0' AND platform_id = p.id
  );

-- Sensor: Temperatura del Aire (var_code=05) → grados Celsius (°C)
-- Reutilizamos la variable "Temperatura Exterior" (id=9) que ya existe en el sistema.
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Temperatura del Aire - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Temperatura Exterior'
  AND u.symbol = '°C'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Temperatura del Aire - CMD0' AND platform_id = p.id
  );

-- Sensor: Velocidad del Viento (var_code=03)
-- La API entrega km/h; el scraper convierte a m/s antes de insertar.
-- Unidad almacenada: m/s (consistente con otras estaciones del sistema).
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Velocidad del Viento - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Velocidad del Viento'
  AND u.symbol = 'm/s'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Velocidad del Viento - CMD0' AND platform_id = p.id
  );

-- Sensor: Dirección del Viento (var_code=02) → grados (°)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
SELECT
    p.id,
    'Sensor de Dirección del Viento - CMD0',
    v.id,
    u.id
FROM
    oogsj_data.platform  p,
    oogsj_data.variable  v,
    oogsj_data.unit      u
WHERE p.name = 'Estación EMAC - Caleta Córdova CMD0'
  AND v.name = 'Dirección del Viento'
  AND u.symbol = '°'
  AND NOT EXISTS (
      SELECT 1 FROM oogsj_data.sensor
      WHERE name = 'Sensor de Dirección del Viento - CMD0' AND platform_id = p.id
  );


-- ─────────────────────────────────────────────────────────────────────────────
-- 6. VERIFICACIÓN FINAL (opcional, no falla si no coincide; solo informa)
--    Ejecutar manualmente para confirmar que todo se insertó correctamente:
--
--    SELECT s.id, s.name, v.name AS variable, u.symbol AS unidad
--    FROM   oogsj_data.sensor s
--    JOIN   oogsj_data.variable v ON v.id = s.variable_id
--    JOIN   oogsj_data.unit     u ON u.id = s.unit_id
--    WHERE  s.platform_id = (
--               SELECT id FROM oogsj_data.platform
--               WHERE name = 'Estación EMAC - Caleta Córdova CMD0'
--           )
--    ORDER BY s.id;
-- ─────────────────────────────────────────────────────────────────────────────

COMMIT;
