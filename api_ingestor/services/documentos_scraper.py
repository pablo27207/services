-- EJEMPLO de inserción de un ítem traído por scraper
WITH d AS (
  INSERT INTO oogsj_data.document(title, year, venue, citations, url, doi)
  VALUES (
    'Doing Journeys - Transatlantische Reisen von Lateinamerika nach Europa schreiben, 1839-1910',
    2021,
    'transcript Verlag eBooks',
    2,
    'https://doi.org/10.1515/9783839456736',
    '10.1515/9783839456736'
  ) RETURNING id
),
aut AS (
  INSERT INTO oogsj_data.author(full_name) VALUES ('Lilli Riettiens')
  ON CONFLICT (full_name) DO NOTHING
  RETURNING id
)
INSERT INTO oogsj_data.document_author(document_id, author_id, author_order)
SELECT (SELECT id FROM d), (SELECT id FROM oogsj_data.author WHERE full_name='Lilli Riettiens'), 1;

INSERT INTO oogsj_data.document_source(document_id, source_type, source_name, raw_payload)
SELECT (SELECT id FROM d),
       'scraper',
       'openalex|custom',
       '{
          "Año": 2021,
          "Citas": 2,
          "Venue": "transcript Verlag eBooks",
          "Autores": ["Lilli Riettiens"],
          "URL": "https://doi.org/10.1515/9783839456736"
        }'::jsonb;
