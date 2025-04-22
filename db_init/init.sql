-- Crear esquema para organizar los datos
CREATE SCHEMA IF NOT EXISTS oogsj_data;

-- Tabla de Quality Flags (Indicadores de Calidad de Datos)
CREATE TABLE oogsj_data.quality_flag (
    id SERIAL PRIMARY KEY,
    flag INT UNIQUE CHECK (flag BETWEEN 0 AND 9),
    description TEXT NOT NULL
);

-- Tabla de Tipos de Plataforma
CREATE TABLE oogsj_data.platform_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- abla de Plataformas (boyas, mareógrafos, etc.)
CREATE TABLE oogsj_data.platform (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform_type_id INT REFERENCES oogsj_data.platform_type(id)
);

-- Tabla de Ubicaciones de la Plataforma (Historial de Movimientos)
CREATE TABLE oogsj_data.platform_location_history (
    id SERIAL PRIMARY KEY,
    platform_id INT REFERENCES oogsj_data.platform(id) ON DELETE CASCADE,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    depth FLOAT,  -- Para plataformas sumergidas
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL  -- NULL significa que es la ubicación actual
);

-- Tabla de Variables de Medición (ej: altura de olas, nivel del mar)
CREATE TABLE oogsj_data.variable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- Tabla de Unidades de Medida (ej: metros, grados Celsius)
CREATE TABLE oogsj_data.unit (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    symbol VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla de Sensores
CREATE TABLE oogsj_data.sensor (
    id SERIAL PRIMARY KEY,
    platform_id INT REFERENCES oogsj_data.platform(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    variable_id INT REFERENCES oogsj_data.variable(id) ON DELETE CASCADE,
    unit_id INT REFERENCES oogsj_data.unit(id) ON DELETE CASCADE,
    calibration_date TIMESTAMP
);

-- Crear tabla de Niveles de Procesamiento
CREATE TABLE oogsj_data.processing_level (
    id SERIAL PRIMARY KEY,
    level VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL
);

-- Tabla de Mediciones
CREATE TABLE oogsj_data.measurement (
    id SERIAL PRIMARY KEY,
    sensor_id INT REFERENCES oogsj_data.sensor(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    value FLOAT NOT NULL,
    quality_flag INT REFERENCES oogsj_data.quality_flag(flag) ON DELETE SET NULL,
    processing_level_id INT REFERENCES oogsj_data.processing_level(id) ON DELETE SET NULL,
    location_id INT REFERENCES oogsj_data.platform_location_history(id) ON DELETE SET NULL,
    UNIQUE (sensor_id, timestamp)
);

-- Insertar Niveles de Procesamiento estándar según recomendaciones del COI
INSERT INTO oogsj_data.processing_level (level, description) VALUES
('Raw', 'Datos crudos sin procesamiento'),
('QC-1', 'Datos revisados con control de calidad básico'),
('QC-2', 'Datos con control de calidad avanzado'),
('Interpolated', 'Datos interpolados para completar lagunas'),
('Model Output', 'Datos provenientes de un modelo numérico'),
('Derived', 'Datos calculados a partir de otros datos medidos');

-- Insertar los Quality Flags según la recomendación del COI
INSERT INTO oogsj_data.quality_flag (flag, description) VALUES
(0, 'No evaluado'), --1
(1, 'Bueno'), --2
(2, 'Probablemente bueno'), --3
(3, 'Sospechoso'), --4
(4, 'Malo'), --5
(5, 'Cambiado'), --6
(6, 'Interpolado'), --7
(7, 'Estimado'), --8
(8, 'Desconocido'), --9
(9, 'Erróneo'); --10

-- Insertar Tipos de Plataforma
INSERT INTO oogsj_data.platform_type (name) VALUES
('Boya Oceanográfica'), --1
('Mareógrafo'), --2
('Modelo Numérico'), --3
('Estación Meteorológica'); --4

-- Insertar Unidades de Medida Comunes
INSERT INTO oogsj_data.unit (name, symbol) VALUES
('Metros', 'm'), --1
('Grados Celsius', '°C'), --2
('Hectopascales', 'hPa'), --3
('Nudos', 'kn'), --4
('Grados', '°'), --5
('Segundos', 's'), --6
('micromol/m2/s', 'µmol/m2/s'), --7
('Volts', 'V'), --8
('Metros por segundo', 'm/s'), --9
('millas/hora', 'mph'), --10
('Unidad desconocida', '?'), --11
('Milímetros', 'mm'), --12
('Días grado Fahrenheit', '°F·d'), --13
('Número de muestras', 'muestras'), --14
('Millas', 'mi'), --15
('Energía solar acumulada', 'Wh/m²'), --16
('Pulgadas de mercurio', 'inHg'), -- 17
('Grados Fahrenheit', '°F'), --18
('Porcentaje', '%'), --19
('Dosis UV acumulada', 'mJ/cm²'), --20
('Índice UV', 'índice'); --21

-- Insertar Variables de Medición
INSERT INTO oogsj_data.variable (name, description) VALUES
('Altura de Olas', 'Altura de las olas medida en metros'), --1
('Periodo de Olas', 'Tiempo entre crestas de olas en segundos'), --2
('Dirección de Olas', 'Ángulo de incidencia de las olas en grados'), --3
('Nivel del Mar', 'Altura de la superficie del mar respecto a un nivel de referencia'), --4
('Velocidad de la corriente', 'Velocidad de la corriente marina en metros por segundo'), --5
('Dirección de la corriente', 'Ángulo de la corriente marina en grados'), --6
('Radiación PAR', 'Radiación fotosintéticamente activa en micromoles por metro cuadrado por segundo'), --7
('Batería', 'Voltaje de la batería en volts'), --8
('Temperatura Exterior', 'Temperatura del aire medida en el ambiente exterior en grados Celsius'), --9
('Humedad Exterior', 'Porcentaje de humedad relativa del aire exterior'), --10
('Presión Barométrica', 'Presión atmosférica medida a nivel de estación en milibares o hectopascales'), --11
('Velocidad del Viento', 'Velocidad del viento en metros por segundo'), --12
('Temp Out', 'Temperatura exterior en grados Celsius (nombre alternativo)'), --13
('Temp Out Hi', 'Temperatura exterior máxima registrada en un periodo dado'), --14
('Temp Out Lo', 'Temperatura exterior mínima registrada en un periodo dado'), --15
('Temp In', 'Temperatura interior en grados Celsius'), --16
('Hum In', 'Humedad relativa del aire en el interior en porcentaje'), --17
('Hum Out', 'Humedad relativa del aire en el exterior (nombre alternativo)'), --18
('Rainfall In', 'Precipitación acumulada medida en pulgadas'), --19
('Rainfall Clicks', 'Número de eventos de medición de lluvia (cada "click" representa una cantidad fija de precipitación)'), --20
('Rainfall Mm', 'Precipitación acumulada medida en milímetros'), --21
('Rain Rate Hi In', 'Tasa máxima de precipitación en pulgadas por hora'), --22
('Rain Rate Hi Clicks', 'Tasa máxima de precipitación registrada en número de clicks'), --23
('Rain Rate Hi Mm', 'Tasa máxima de precipitación en milímetros por hora'), --24
('Et', 'Evapotranspiración estimada en milímetros'), --25
('Bar', 'Presión barométrica registrada (nombre abreviado)'), --26
('Wind Num Samples', 'Número de muestras de velocidad/dirección de viento recolectadas'), --27
('Wind Speed Avg', 'Velocidad promedio del viento en un intervalo dado'), --28
('Wind Speed Hi', 'Velocidad máxima del viento registrada'), --29
('Wind Dir Of Hi', 'Dirección del viento cuando se registró la velocidad máxima'), --30
('Wind Dir Of Prevail', 'Dirección predominante del viento durante un periodo'), --31
('Abs Press', 'Presión atmosférica absoluta en milibares o hectopascales'), --32
('Bar Noaa', 'Presión barométrica ajustada al nivel del mar según estándar NOAA'), --33
('Bar Alt', 'Presión barométrica ajustada por altitud'), --34
('Dew Point Out', 'Temperatura de rocío en el exterior'), --35
('Dew Point In', 'Temperatura de rocío en el interior'), --36
('Emc', 'Contenido de humedad de equilibrio en porcentaje'), --37
('Heat Index Out', 'Índice de calor exterior que combina temperatura y humedad'), --38
('Heat Index In', 'Índice de calor interior que combina temperatura y humedad'), --39
('Wind Chill', 'Sensación térmica exterior considerando temperatura y viento'), --40
('Wind Run', 'Distancia total recorrida por el viento durante un periodo, en kilómetros o millas'), --41
('Deg Days Heat', 'Grados-día de calefacción acumulados (Heating Degree Days)'), --42
('Deg Days Cool', 'Grados-día de refrigeración acumulados (Cooling Degree Days)'), --43
('Thw Index', 'Índice THW (Temperatura, Humedad y Viento) que refleja sensación térmica'), --44
('Wet Bulb', 'Temperatura de bulbo húmedo que considera evaporación y enfriamiento'), --45
('Solar Rad Avg', 'Radiación solar promedio en vatios por metro cuadrado'), --46
('Solar Rad Hi', 'Radiación solar máxima registrada'), --47
('Uv Index Avg', 'Índice UV promedio durante el día'), --48
('Uv Index Hi', 'Índice UV máximo registrado'), --49
('Solar Energy', 'Energía solar total recibida en kilojulios por metro cuadrado'), --50
('Uv Dose', 'Dosis total de radiación UV acumulada durante el día'), --51
('Night Cloud Cover', 'Porcentaje estimado de cobertura nubosa durante la noche'), --52
('Thsw Index', 'Índice THSW (Temperatura, Humedad, Sol y Viento), una medida de sensación térmica extendida'), --53
('Temp Extra 1', 'Temperatura registrada por un sensor adicional externo'); --54


INSERT INTO oogsj_data.platform (name, platform_type_id)VALUES 
('Mareógrafo - Puerto Comodoro Rivadavia', 2), --1
('Predicción de Marea - Hidrografía Naval', 3), --2
('Boya CIDMAR-2', 1), --3
('APPCR Puerto CR', 4), --4
('APPCR Muelle CC', 4); --5


INSERT INTO oogsj_data.platform_location_history (platform_id, latitude, longitude, depth, start_time) VALUES
(1, -45.860509, -67.466166, 0, '2025-01-01'), --1 Mareógrafo - Puerto Comodoro Rivadavia
(3, -45.877486, -67.442217, 0, '2025-01-01 00:00:00'), --2 Boya CIDMAR-2
(4, -45.862220, -67.463340, 0, '2023-06-02 00:00:00'), --3 APPCR Puerto CR
(5, -45.836000, -67.646670, 0, '2025-01-01 00:00:00'); --4 APPCR Muelle CC


INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id) VALUES 
(1, 'Valeport TideMaster', 4, 1),
(2, 'Modelo de Predicción de Mareas - Hidrografía Naval', 4, 1),
(3, 'Sensor de Altura de Olas - CIDMAR-2', 1, 1),
(3, 'Sensor de Periodo de Olas - CIDMAR-2', 2, 5),
(3, 'Sensor de Dirección de Olas - CIDMAR-2', 3, 18),
(3, 'Sensor de Velocidad de Corriente - CIDMAR-2', 5, 8),
(3, 'Sensor de Dirección de la Corriente - CIDMAR-2', 6, 18),
(3, 'Sensor de Radiación PAR - CIDMAR-2', 7, 6),
(3, 'Sensor de Batería - CIDMAR-2', 8, 7),
(4,'temp_out - 160710', 9, 2),
(4,'hum_out - 160710', 10, 14),
(4,'bar - 160710', 11, 3),
(4,'wind_speed - 160710', 12, 8),
(4,'temp_out_hi - 160710', 14, 2),
(4,'temp_out_lo - 160710', 15, 2),
(4,'temp_in - 160710', 16, 2),
(4,'dew_point_out - 160710', 35, 2),
(4,'dew_point_in - 160710', 36, 2),
(4,'heat_index_out - 160710', 38, 2),
(4,'heat_index_in - 160710', 39, 2),
(4,'wind_chill - 160710', 40, 2),
(4,'thw_index - 160710', 44, 2),
(4,'wet_bulb - 160710', 45, 2),
(4,'hum_in - 160710', 17, 14),
(4,'emc - 160710', 37, 14),
(4,'abs_press - 160710', 32, 3),
(4,'bar_noaa - 160710', 33, 3),
(4,'bar_alt - 160710', 34, 3),
(4,'rainfall_clicks - 160710', 20, 16),
(4,'rainfall_mm - 160710', 21, 9),
(4,'rain_rate_hi_clicks - 160710', 23, 16),
(4,'rain_rate_hi_mm - 160710', 24, 10),
(4,'et - 160710', 25, 9),
(4,'wind_dir_of_hi - 160710', 30, 18),
(4,'wind_dir_of_prevail - 160710', 31, 18),
(4,'wind_speed_avg - 160710', 28, 8),
(4,'wind_speed_hi - 160710', 29, 8),
(4,'wind_run - 160710', 41, 11),
(4,'wind_num_samples - 160710', 27, 16),
(4,'deg_days_heat - 160710', 42, 9),
(4,'deg_days_cool - 160710', 43, 9),
(5,'temp_in - 191512', 16, 2),
(5,'rainfall_clicks - 191512', 20, 16),
(5,'rainfall_mm - 191512', 21, 9),
(5,'rain_rate_hi_clicks - 191512', 23, 16),
(5,'rain_rate_hi_mm - 191512', 24, 10),
(5,'et - 191512', 25, 9),
(5,'wind_num_samples - 191512', 27, 16),
(5,'wind_speed_avg - 191512', 28, 8),
(5,'wind_speed_hi - 191512', 29, 8),
(5,'wind_dir_of_hi - 191512', 30, 18),
(5,'wind_dir_of_prevail - 191512', 31, 18),
(5,'solar_rad_avg - 191512', 46, 12),
(5,'solar_rad_hi - 191512', 47, 12),
(5,'solar_energy - 191512', 50, 13),
(5,'bar - 191512', 26, 3),
(5,'hum_out - 191512', 18, 14),
(5,'temp_out - 191512', 13, 2),
(5,'thsw_index - 191512', 53, 2),
(5,'night_cloud_cover - 191512', 52, 14),
(5,'uv_dose - 191512', 51, 17),
(5,'uv_index_avg - 191512', 48, 15),
(5,'uv_index_hi - 191512', 49, 15),
(5,'abs_press - 191512', 32, 3),
(5,'bar_noaa - 191512', 33, 3),
(5,'bar_alt - 191512', 34, 3),
(5,'wind_run - 191512', 41, 11),
(5,'temp_out_hi - 191512', 14, 2),
(5,'temp_out_lo - 191512', 15, 2),
(5,'wind_chill - 191512', 40, 2),
(5,'deg_days_heat - 191512', 42, 9),
(5,'deg_days_cool - 191512', 43, 9),
(5,'heat_index_out - 191512', 38, 2),
(5,'thw_index - 191512', 44, 2),
(5,'dew_point_out - 191512', 35, 2),
(5,'wet_bulb - 191512', 45, 2),
(4,'temp_extra_1 - 160710', 54, 2);