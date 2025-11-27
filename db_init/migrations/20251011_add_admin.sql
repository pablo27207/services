BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Flag admin y pass hash (si no existen)
ALTER TABLE oogsj_data."user"
  ADD COLUMN IF NOT EXISTS password_hash TEXT,
  ADD COLUMN IF NOT EXISTS is_admin boolean DEFAULT false;

-- Índice útil para búsquedas por email
CREATE INDEX IF NOT EXISTS idx_user_email_lower
  ON oogsj_data."user"(LOWER(email));

-- Usuario admin inicial (tu usuario)
INSERT INTO oogsj_data."user"
(first_name, last_name, dni, email, password_hash, is_admin, role_id, workplace_id)
VALUES (
  'Franco Maximiliano',
  'García González',
  '39437205',
  'gfranco323@gmail.com',
  crypt('Mamalesa21', gen_salt('bf')),
  true,
  (SELECT id FROM oogsj_data.role WHERE name='Administrador'),
  (SELECT id FROM oogsj_data.workplace WHERE name='Agencia Comodoro Conocimiento')
)
ON CONFLICT (email) DO UPDATE
SET password_hash = EXCLUDED.password_hash,
    is_admin      = true,
    role_id       = COALESCE(EXCLUDED.role_id, oogsj_data."user".role_id),
    workplace_id  = COALESCE(EXCLUDED.workplace_id, oogsj_data."user".workplace_id);

COMMIT;
