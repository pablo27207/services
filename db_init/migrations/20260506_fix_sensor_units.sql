-- Corrección de unit_ids incorrectos en sensores de plataformas meteorológicas.
-- Afecta: APPCR Muelle CC (platform_id=5, station 191512)
--         APPCR Puerto CR (platform_id=4, station 160710)
-- Los unit_ids estaban mezclados al cargar el init.sql original.

-- Nueva unidad necesaria para radiación solar instantánea
INSERT INTO oogsj_data.unit (name, symbol)
VALUES ('Vatios por metro cuadrado', 'W/m²')
ON CONFLICT (symbol) DO NOTHING;

-- ── APPCR Muelle CC (station 191512) ─────────────────────────────────────────

-- Velocidad de viento: V → m/s
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'm/s')
WHERE name IN ('wind_speed_avg - 191512', 'wind_speed_hi - 191512');

-- Dirección de viento: °F → °
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '°')
WHERE name IN ('wind_dir_of_hi - 191512', 'wind_dir_of_prevail - 191512');

-- Precipitación en clicks: Wh/m² → muestras
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'muestras')
WHERE name IN ('rainfall_clicks - 191512', 'rain_rate_hi_clicks - 191512', 'wind_num_samples - 191512');

-- Precipitación en mm: m/s → mm
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'mm')
WHERE name IN ('rainfall_mm - 191512', 'rain_rate_hi_mm - 191512', 'et - 191512');

-- Humedad relativa: muestras → %
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '%')
WHERE name = 'hum_out - 191512';

-- Radiación solar promedio/máxima: mm → W/m²
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'W/m²')
WHERE name IN ('solar_rad_avg - 191512', 'solar_rad_hi - 191512');

-- Energía solar acumulada: °F·d → Wh/m²
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'Wh/m²')
WHERE name = 'solar_energy - 191512';

-- Dosis UV: inHg → mJ/cm²
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'mJ/cm²')
WHERE name = 'uv_dose - 191512';

-- Índice UV: mi → índice
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'índice')
WHERE name IN ('uv_index_avg - 191512', 'uv_index_hi - 191512');

-- Grados-día calefacción/refrigeración: m/s → °F·d
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '°F·d')
WHERE name IN ('deg_days_heat - 191512', 'deg_days_cool - 191512');

-- ── APPCR Puerto CR (station 160710) ─────────────────────────────────────────

-- Velocidad de viento: V → m/s
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'm/s')
WHERE name IN ('wind_speed - 160710', 'wind_speed_avg - 160710', 'wind_speed_hi - 160710');

-- Dirección de viento: °F → °
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '°')
WHERE name IN ('wind_dir_of_hi - 160710', 'wind_dir_of_prevail - 160710');

-- Precipitación en clicks: Wh/m² → muestras
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'muestras')
WHERE name IN ('rainfall_clicks - 160710', 'rain_rate_hi_clicks - 160710', 'wind_num_samples - 160710');

-- Precipitación en mm: m/s o mph → mm
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = 'mm')
WHERE name IN ('rainfall_mm - 160710', 'rain_rate_hi_mm - 160710', 'et - 160710');

-- Humedad relativa: muestras → %
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '%')
WHERE name = 'hum_out - 160710';

-- Grados-día calefacción/refrigeración: m/s → °F·d
UPDATE oogsj_data.sensor SET unit_id = (SELECT id FROM oogsj_data.unit WHERE symbol = '°F·d')
WHERE name IN ('deg_days_heat - 160710', 'deg_days_cool - 160710');
