-- usuarios
INSERT INTO oogsj_data."user"(first_name,last_name,dni,email,role_id,workplace_id) VALUES
('Juan','Pérez','30123456','juan.perez@ejemplo.org',
 (SELECT id FROM oogsj_data.role WHERE name='Investigador'),
 (SELECT id FROM oogsj_data.workplace WHERE name='Agencia Comodoro Conocimiento')
),
('Ana','Torres','28999888','ana.torres@ejemplo.org',
 (SELECT id FROM oogsj_data.role WHERE name='Técnico'),
 (SELECT id FROM oogsj_data.workplace WHERE name='UNPSJB')
)
ON CONFLICT (email) DO NOTHING;

-- paper 1 (subido por Juan)
WITH d AS (
  INSERT INTO oogsj_data.document(title, year, venue, citations, url, doi, storage_path)
  VALUES (
    'Dinámica de mareas y validación con mareógrafos locales en el Golfo San Jorge',
    2025,'Revista Patagónica de Oceanografía',0,
    'https://oogsj.gob.ar/papers/dinamica-mareas-gsj','10.1234/gsj.2025.001',
    '/data/docs/dinamica_mareas_gsj.pdf'
  )
  ON CONFLICT (doi) DO NOTHING
  RETURNING id
)
INSERT INTO oogsj_data.author(full_name) VALUES ('Juan Pérez') ON CONFLICT (full_name) DO NOTHING;
INSERT INTO oogsj_data.author(full_name) VALUES ('Ana Torres') ON CONFLICT (full_name) DO NOTHING;
INSERT INTO oogsj_data.document_author(document_id, author_id, author_order)
SELECT d.id, a.id, x.ord
FROM (VALUES ('Juan Pérez',1),('Ana Torres',2)) AS x(name,ord)
JOIN oogsj_data.author a ON a.full_name=x.name
JOIN (SELECT COALESCE((SELECT id FROM d), (SELECT id FROM oogsj_data.document WHERE doi='10.1234/gsj.2025.001')) AS id) d ON true
ON CONFLICT DO NOTHING;

INSERT INTO oogsj_data.document_source(document_id, source_type, uploaded_by, source_name)
SELECT d.id, 'user_upload',
       (SELECT id FROM oogsj_data."user" WHERE email='juan.perez@ejemplo.org'),
       'carga manual'
FROM oogsj_data.document d WHERE d.doi='10.1234/gsj.2025.001'
ON CONFLICT DO NOTHING;

-- paper 2 (subido por Ana)
WITH d AS (
  INSERT INTO oogsj_data.document(title, year, venue, citations, url, doi, storage_path)
  VALUES (
    'Arquitectura de un observatorio oceanográfico abierto: de sensores a tablero público',
    2024,'Boletín de Sistemas y Datos Ambientales',3,
    'https://oogsj.gob.ar/papers/arquitectura-observatorio','10.4321/oogsj.2024.042',
    '/data/docs/arquitectura_observatorio.pdf'
  )
  ON CONFLICT (doi) DO NOTHING
  RETURNING id
)
INSERT INTO oogsj_data.author(full_name) VALUES ('Carlos Gómez') ON CONFLICT (full_name) DO NOTHING;
INSERT INTO oogsj_data.author(full_name) VALUES ('Ana Torres')   ON CONFLICT (full_name) DO NOTHING;
INSERT INTO oogsj_data.document_author(document_id, author_id, author_order)
SELECT d.id, a.id, x.ord
FROM (VALUES ('Ana Torres',1),('Carlos Gómez',2)) AS x(name,ord)
JOIN oogsj_data.author a ON a.full_name=x.name
JOIN (SELECT COALESCE((SELECT id FROM d), (SELECT id FROM oogsj_data.document WHERE doi='10.4321/oogsj.2024.042')) AS id) d ON true
ON CONFLICT DO NOTHING;

INSERT INTO oogsj_data.document_source(document_id, source_type, uploaded_by, source_name)
SELECT d.id, 'user_upload',
       (SELECT id FROM oogsj_data."user" WHERE email='ana.torres@ejemplo.org'),
       'carga manual'
FROM oogsj_data.document d WHERE d.doi='10.4321/oogsj.2024.042'
ON CONFLICT DO NOTHING;
