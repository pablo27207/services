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
(0, 'No evaluado'),
(1, 'Bueno'),
(2, 'Probablemente bueno'),
(3, 'Sospechoso'),
(4, 'Malo'),
(5, 'Cambiado'),
(6, 'Interpolado'),
(7, 'Estimado'),
(8, 'Desconocido'),
(9, 'Erróneo');

-- Insertar Tipos de Plataforma
INSERT INTO oogsj_data.platform_type (name) VALUES
('Boya Oceanográfica'),
('Mareógrafo'),
('Modelo Numérico');

-- Insertar Unidades de Medida Comunes
INSERT INTO oogsj_data.unit (name, symbol) VALUES
('Metros', 'm'),
('Grados Celsius', '°C'),
('Hectopascales', 'hPa'),
('Nudos', 'kn'),
('Grados', '°'),
('Segundos', 's'),
('micromol/m2/s', 'µmol/m2/s'),
('Volts', 'V'),
('Metros por segundo', 'm/s');

-- Insertar Variables de Medición
INSERT INTO oogsj_data.variable (name, description) VALUES
('Altura de Olas', 'Altura de las olas medida en metros'),
('Periodo de Olas', 'Tiempo entre crestas de olas en segundos'),
('Dirección de Olas', 'Ángulo de incidencia de las olas en grados'),
('Nivel del Mar', 'Altura de la superficie del mar respecto a un nivel de referencia'),
('Velocidad de la corriente', 'Velocidad de la corriente marina en metros por segundo'),
('Dirección de la corriente', 'Ángulo de la corriente marina en grados'),
('Radiación PAR', 'Radiación fotosintéticamente activa en micromoles por metro cuadrado por segundo'),
('Batería', 'Voltaje de la batería en volts');

-- DATOS DE MAREOGRAFO --

-- Insertar la plataforma del Mareógrafo
INSERT INTO oogsj_data.platform (name, platform_type_id)
VALUES ('Mareógrafo - Puerto Comodoro Rivadavia', 2)
RETURNING id;

-- Insertar la ubicación geográfica del Mareógrafo
INSERT INTO oogsj_data.platform_location_history (platform_id, latitude, longitude, depth, start_time)
VALUES (1, -45.860509, -67.466166, 0, '2025-01-01')
RETURNING id;

-- Insertar el sensor del Mareógrafo
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
VALUES (1, 'Valeport TideMaster', 4, 1)
RETURNING id;


-- DATOS DE PREDICCION DE MAREA HIDROGRAFIA NAVAL ---

-- Insertar la plataforma para Predicción de Marea
INSERT INTO oogsj_data.platform (name, platform_type_id)
VALUES ('Predicción de Marea - Hidrografía Naval', 3)
RETURNING id;


-- Insertar el "sensor" para la predicción de marea (en realidad representa el modelo)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
VALUES (2, 'Modelo de Predicción de Mareas - Hidrografía Naval', 4, 1)
RETURNING id;

-- DATOS DE BOYA OCEANOGRAFICA --   
INSERT INTO oogsj_data.platform (name, platform_type_id)
VALUES (' Boya CIDMAR-2', 1)
RETURNING id;

-- Insertar la ubicación de la boya CIDMAR-2 
INSERT INTO oogsj_data.platform_location_history (platform_id, latitude, longitude, depth, start_time)
VALUES (3, -45.877486, -67.442217, 0, '2025-01-01')
RETURNING id;

--  Insertar sensores de la boya (cada variable con su unidad correspondiente)
INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
VALUES
(3, 'Sensor de Altura de Olas - CIDMAR-2', 1, 1),  -- Metros
(3, 'Sensor de Periodo de Olas - CIDMAR-2', 2, 6),  -- Segundos
(3, 'Sensor de Dirección de Olas - CIDMAR-2', 3, 5),  -- Grados
(3, 'Sensor de Velocidad de Corriente - CIDMAR-2', 5, 9),  -- m/s
(3, 'Sensor de Dirección de la Corriente - CIDMAR-2', 6, 5),  -- Grados
(3, 'Sensor de Radiación PAR - CIDMAR-2', 7, 7),  -- micromol / (m2 / s)
(3, 'Sensor de Batería - CIDMAR-2', 8, 8)  -- Volts
RETURNING id;