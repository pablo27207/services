-- Migración: Tablas especie y noticia
-- Fecha: 2026-04-22

CREATE TABLE IF NOT EXISTS oogsj_data.especie (
    id                SERIAL PRIMARY KEY,
    nombre_comun      VARCHAR(200) NOT NULL,
    nombre_cientifico VARCHAR(200),
    descripcion       TEXT,
    categoria         VARCHAR(100),
    imagen_url        TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS oogsj_data.noticia (
    id         SERIAL PRIMARY KEY,
    titulo     VARCHAR(300) NOT NULL,
    contenido  TEXT NOT NULL,
    categoria  VARCHAR(100),
    imagen_url TEXT,
    publicado  BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
