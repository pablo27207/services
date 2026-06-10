-- Agrega modo mantenimiento a plataformas (idempotente con IF NOT EXISTS)
ALTER TABLE oogsj_data.platform
    ADD COLUMN IF NOT EXISTS maintenance_mode    BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS maintenance_message TEXT;
