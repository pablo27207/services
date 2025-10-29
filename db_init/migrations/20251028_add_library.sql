BEGIN;

-- Catálogos
CREATE TABLE IF NOT EXISTS oogsj_data.role (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS oogsj_data.workplace (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);

-- Usuarios
CREATE TABLE IF NOT EXISTS oogsj_data."user" (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(120) NOT NULL,
  last_name  VARCHAR(120) NOT NULL,
  dni        VARCHAR(20)  UNIQUE NOT NULL,
  email      VARCHAR(255) UNIQUE NOT NULL,
  role_id    INT REFERENCES oogsj_data.role(id) ON DELETE SET NULL,
  workplace_id INT REFERENCES oogsj_data.workplace(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Autores externos
CREATE TABLE IF NOT EXISTS oogsj_data.author (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(255) UNIQUE NOT NULL
);

-- Documentos/papers
CREATE TABLE IF NOT EXISTS oogsj_data.document (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  year INT CHECK (year BETWEEN 1000 AND 2100),
  venue TEXT,
  citations INT DEFAULT 0 CHECK (citations >= 0),
  url TEXT,
  doi TEXT,
  storage_path TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Autores por documento (N:N con orden)
CREATE TABLE IF NOT EXISTS oogsj_data.document_author (
  document_id INT REFERENCES oogsj_data.document(id) ON DELETE CASCADE,
  author_id   INT REFERENCES oogsj_data.author(id)   ON DELETE RESTRICT,
  author_order INT NOT NULL CHECK (author_order >= 1),
  PRIMARY KEY (document_id, author_id),
  UNIQUE (document_id, author_order)
);

-- Fuente/procedencia (user_upload | scraper | manual)
CREATE TABLE IF NOT EXISTS oogsj_data.document_source (
  id SERIAL PRIMARY KEY,
  document_id INT REFERENCES oogsj_data.document(id) ON DELETE CASCADE,
  source_type VARCHAR(30) NOT NULL CHECK (source_type IN ('user_upload','scraper','manual')),
  uploaded_by INT NULL REFERENCES oogsj_data."user"(id) ON DELETE SET NULL,
  source_name TEXT,
  raw_payload JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_user_email       ON oogsj_data."user"(email);
CREATE INDEX IF NOT EXISTS idx_document_year    ON oogsj_data.document(year);
CREATE INDEX IF NOT EXISTS idx_document_doi     ON oogsj_data.document(doi);
CREATE INDEX IF NOT EXISTS idx_docsource_type   ON oogsj_data.document_source(source_type);

-- Seeds mínimos
INSERT INTO oogsj_data.role (name) VALUES ('Investigador') ON CONFLICT (name) DO NOTHING;
INSERT INTO oogsj_data.role (name) VALUES ('Técnico')      ON CONFLICT (name) DO NOTHING;
INSERT INTO oogsj_data.workplace (name) VALUES ('Agencia Comodoro Conocimiento') ON CONFLICT (name) DO NOTHING;
INSERT INTO oogsj_data.workplace (name) VALUES ('UNPSJB')                         ON CONFLICT (name) DO NOTHING;

COMMIT;
