CREATE TABLE IF NOT EXISTS mareograph_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL UNIQUE,
    level REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS buoy_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    variable TEXT NOT NULL,
    value REAL NOT NULL,
    UNIQUE (timestamp, variable)
);

CREATE TABLE IF NOT EXISTS tide_forecast (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL UNIQUE,
    level REAL NOT NULL
);
