-- Agrega columna admin_role a la tabla user.
-- 'master' = administrador completo (puede crear/eliminar usuarios, modificar todo)
-- 'viewer' = solo lectura del dashboard admin (no puede modificar nada)

ALTER TABLE oogsj_data."user"
    ADD COLUMN IF NOT EXISTS admin_role VARCHAR(20) DEFAULT 'master';

-- El admin existente pasa a ser 'master'
UPDATE oogsj_data."user"
SET admin_role = 'master'
WHERE is_admin = true;

-- Los usuarios sin rol admin quedan con NULL (no son admins)
UPDATE oogsj_data."user"
SET admin_role = NULL
WHERE is_admin = false OR is_admin IS NULL;
