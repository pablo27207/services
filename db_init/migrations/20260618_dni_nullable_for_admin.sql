-- Los usuarios admin creados desde el panel no tienen DNI obligatorio.
-- El DNI es requerido solo para usuarios de plataforma científica.
ALTER TABLE oogsj_data."user"
    ALTER COLUMN dni DROP NOT NULL,
    ALTER COLUMN first_name DROP NOT NULL,
    ALTER COLUMN last_name DROP NOT NULL;
