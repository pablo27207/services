CREATE TABLE IF NOT EXISTS oogsj_data.aviso_navegante (
    id          SERIAL PRIMARY KEY,
    numero      VARCHAR(20)  NOT NULL,
    fecha       DATE         NOT NULL,
    tipo        VARCHAR(100),
    texto_es    TEXT,
    texto_en    TEXT,
    fuente      VARCHAR(100) DEFAULT 'SHN - Geoportal',
    scraped_at  TIMESTAMPTZ  DEFAULT NOW(),
    CONSTRAINT  aviso_navegante_numero_unique UNIQUE (numero)
);

CREATE INDEX IF NOT EXISTS idx_aviso_navegante_fecha
    ON oogsj_data.aviso_navegante (fecha DESC);

CREATE INDEX IF NOT EXISTS idx_aviso_navegante_scraped
    ON oogsj_data.aviso_navegante (scraped_at DESC);