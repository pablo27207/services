BEGIN;

-- 1) Extensión para hash bcrypt
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2) Auth: columna de password (hash)
ALTER TABLE oogsj_data."user"
  ADD COLUMN IF NOT EXISTS password_hash TEXT;

-- Si hubiera usuarios sin password aún, setear temporal
UPDATE oogsj_data."user"
SET password_hash = crypt('cambiar_esta_clave', gen_salt('bf'))
WHERE password_hash IS NULL;

-- 3) Rol admin y workplace (por si faltan)
INSERT INTO oogsj_data.role (name) VALUES ('Administrador')
ON CONFLICT (name) DO NOTHING;

INSERT INTO oogsj_data.workplace (name) VALUES ('Agencia Comodoro Conocimiento')
ON CONFLICT (name) DO NOTHING;

-- 4) Tu usuario administrador (usa bcrypt)
--    Cambiá la clave 'AdminFranco!2025' cuando quieras
INSERT INTO oogsj_data."user"
(first_name, last_name, dni, email, password_hash, role_id, workplace_id)
VALUES (
  'Franco Maximiliano',
  'García González',
  '39437205',
  'gfranco323@gmail.com',
  crypt('AdminFranco!2025', gen_salt('bf')),
  (SELECT id FROM oogsj_data.role WHERE name='Administrador'),
  (SELECT id FROM oogsj_data.workplace WHERE name='Agencia Comodoro Conocimiento')
)
ON CONFLICT (email) DO UPDATE
SET password_hash = EXCLUDED.password_hash,
    role_id       = EXCLUDED.role_id,
    workplace_id  = EXCLUDED.workplace_id;

-- 5) Unicidad por DOI (si hay)
CREATE UNIQUE INDEX IF NOT EXISTS uq_document_doi
  ON oogsj_data.document(doi)
  WHERE doi IS NOT NULL;

-- 6) Seed de 10 documentos (referencias + URL)
INSERT INTO oogsj_data.document (title, year, venue, citations, url, doi) VALUES
('Network analysis suggests changes in food web stability in the San Jorge Gulf', 2022, 'Scientific Reports', NULL, 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9237026/', NULL),
('Physico-chemical characterization of the benthic environment of the Golfo San Jorge, Argentina', 2005, 'Journal of the Marine Biological Association of the UK', NULL, 'https://doi.org/10.1017/S002531540501249X', '10.1017/S002531540501249X'),
('Seabird association with shrimp trawlers in Golfo San Jorge (Patagonia, Argentina)', 2011, 'Marine Ecology Progress Series', NULL, 'https://www.int-res.com/articles/meps2011/432/m432p125.pdf', NULL),
('Caracterización de los fondos de pesca del langostino patagónico Pleoticus muelleri en el Golfo San Jorge y litoral de Chubut', 1997, 'Informe técnico (AquaDocs)', NULL, 'https://aquadocs.org/items/04684153-ecdb-4c80-9187-dc9afb427be9', NULL),
('Comparative diets of macrocrustacean species from the San Jorge Gulf, Argentina', 2025, 'Marine and Fisheries (INIDEP)', NULL, 'https://ojs.inidep.edu.ar/index.php/mafis/en/article/view/414', NULL),
('Petroleum generation and accumulation in the Golfo San Jorge Basin', 2001, 'Marine and Petroleum Geology', NULL, 'https://www.sciencedirect.com/science/article/abs/pii/S0264817201000381', NULL),
('The origin of the San Jorge Gulf Basin in the context of the Patagonian broken foreland', 2020, 'Tectonophysics', NULL, 'https://www.sciencedirect.com/science/article/abs/pii/S0895981119304316', NULL),
('Late Cretaceous palynomorphs from the Golfo San Jorge Basin (Cañadón Seco Fm., La Frieda Oeste x-1)', 2021, 'Journal of South American Earth Sciences', NULL, 'https://www.sciencedirect.com/science/article/abs/pii/S0895981120306933', NULL),
('Modern foraminifera from coastal settings in northern San Jorge Gulf (Argentina)', 2011, 'Andean Geology / SciELO', NULL, 'https://ref.scielo.org/c4y82y', NULL),
('Evolution of the San Jorge Basin, Argentina', 1990, 'AAPG Bulletin', NULL, 'https://pubs.geoscienceworld.org/aapg/aapgbull/article/74/6/879/38573/Evolution-of-the-San-Jorge-Basin-Argentina1', NULL)
ON CONFLICT DO NOTHING;

COMMIT;
