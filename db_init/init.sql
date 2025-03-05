CREATE TABLE IF NOT EXISTS mareograph_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL UNIQUE,
    level REAL NOT NULL
);


