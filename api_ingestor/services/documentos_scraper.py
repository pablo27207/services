import os
import time
import logging
import requests
from typing import Dict, List, Optional, Tuple
from psycopg2.extras import Json
from .db_handler import DBHandler

# --------------------------
# Configuración de logging
# --------------------------
logging.basicConfig(
    filename="documents_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------
# Utilidades de entorno
# --------------------------
MAILTO = os.getenv("OPENALEX_MAILTO", "oogsj@example.org")
QUERIES_RAW = os.getenv("SCI_DOC_QUERIES", "Golfo San Jorge; San Jorge Gulf; Patagonia oceanography")
QUERIES = [q.strip() for q in QUERIES_RAW.split(";") if q.strip()]
PER_PAGE = int(os.getenv("SCI_DOC_PER_PAGE", "25"))
MAX_PAGES = int(os.getenv("SCI_DOC_MAX_PAGES", "2"))
REQUEST_TIMEOUT = 15
REQUEST_DELAY_S = 1.0  # entre páginas para no golpear la API

OPENALEX_BASE = "https://api.openalex.org/works"

class ScientificDocScraper:
    """
    Scraper de metadatos científicos usando OpenAlex:
      - Solo almacena metadatos en tu esquema (document, author, document_author)
      - Registra procedencia en document_source (source_type='scraper', source_name='openalex')
      - Idempotente: upsert por DOI; sin DOI usa heurística (title+year+primer autor)
    """

    @staticmethod
    def _normalize_title(title: Optional[str]) -> Optional[str]:
        if not title:
            return None
        t = " ".join(title.split()).strip()
        return t if t else None

    @staticmethod
    def _extract_fields(item: Dict) -> Dict:
        """Mapea un registro OpenAlex a nuestro payload interno normalizado."""
        # Título
        title = ScientificDocScraper._normalize_title(item.get("title"))

        # Año
        year = item.get("publication_year")
        try:
            if year is not None:
                year = int(year)
                if year < 1000 or year > 2100:
                    year = None
        except Exception:
            year = None

        # Venue (revista/conferencia)
        venue = None
        host_venue = item.get("host_venue") or {}
        if isinstance(host_venue, dict):
            venue = host_venue.get("display_name")
            venue = ScientificDocScraper._normalize_title(venue)

        # Citations
        citations = item.get("cited_by_count")
        try:
            citations = int(citations) if citations is not None else None
            if citations is not None and citations < 0:
                citations = None
        except Exception:
            citations = None

        # DOI (id.doi viene como 'https://doi.org/xxx' o puede venir en 'doi')
        doi = None
        ids = item.get("ids") or {}
        if isinstance(ids, dict):
            doi_url = ids.get("doi")
            if doi_url and isinstance(doi_url, str) and "doi.org/" in doi_url:
                doi = doi_url.split("doi.org/")[-1].strip()
        # fallback (algunos items traen 'doi' plano)
        if not doi:
            raw_doi = item.get("doi")
            if raw_doi and isinstance(raw_doi, str):
                doi = raw_doi.replace("https://doi.org/", "").strip()

        doi = doi if doi else None

        # URL preferente: DOI si hay, si no landing
        url = None
        if doi:
            url = f"https://doi.org/{doi}"
        if not url:
            primary = item.get("primary_location") or {}
            if isinstance(primary, dict):
                url = primary.get("landing_page_url")

        # Autores (orden original)
        authors: List[str] = []
        authorships = item.get("authorships") or []
        for au in authorships:
            a = (au or {}).get("author") or {}
            name = a.get("display_name")
            name = ScientificDocScraper._normalize_title(name)
            if name:
                authors.append(name)

        return {
            "title": title,
            "year": year,
            "venue": venue,
            "citations": citations,
            "authors": authors,  # ordenados
            "url": url,
            "doi": doi,
            "raw": item
        }

    # --------------------------
    # Llamadas a OpenAlex
    # --------------------------
    @staticmethod
    def _fetch_openalex_page(query: str, cursor: str = "*") -> Dict:
        params = {
            "search": query,
            "per_page": PER_PAGE,
            "cursor": cursor,
            "mailto": MAILTO
        }
        r = requests.get(OPENALEX_BASE, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _iter_openalex_results(query: str):
        """Itera páginas de OpenAlex con cursor hasta MAX_PAGES."""
        cursor = "*"
        pages = 0
        while pages < MAX_PAGES:
            data = ScientificDocScraper._fetch_openalex_page(query, cursor)
            results = data.get("results", [])
            for item in results:
                yield item
            cursor = data.get("meta", {}).get("next_cursor")
            pages += 1
            if not cursor:
                break
            time.sleep(REQUEST_DELAY_S)

    # --------------------------
    # DB helpers
    # --------------------------
    @staticmethod
    def _ensure_author(cur, name: str) -> int:
        cur.execute("SELECT id FROM oogsj_data.author WHERE full_name = %s", (name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute(
            "INSERT INTO oogsj_data.author (full_name) VALUES (%s) RETURNING id",
            (name,)
        )
        return cur.fetchone()[0]

    @staticmethod
    def _find_document_without_doi(cur, title: str, year: Optional[int], first_author: Optional[str]) -> Optional[int]:
        """
        Heurística: mismo título (case-insensitive) y año y primer autor (si lo hay).
        """
        params: List = [title]
        sql = """
            SELECT d.id
            FROM oogsj_data.document d
            WHERE LOWER(d.title) = LOWER(%s)
        """
        if year is not None:
            sql += " AND d.year = %s"
            params.append(year)
        if first_author:
            sql += """
                AND EXISTS (
                    SELECT 1
                    FROM oogsj_data.document_author da
                    JOIN oogsj_data.author a ON a.id = da.author_id
                    WHERE da.document_id = d.id
                      AND da.author_order = 1
                      AND a.full_name = %s
                )
            """
            params.append(first_author)

        cur.execute(sql, tuple(params))
        row = cur.fetchone()
        return row[0] if row else None

    @staticmethod
    def _upsert_document(cur, doc: Dict) -> Tuple[int, bool]:
        """
        Inserta o actualiza documento.
        Devuelve (document_id, created_bool)
        Política: no sobreescribir con NULL campos existentes.
        """
        title = doc["title"]
        year = doc["year"]
        venue = doc["venue"]
        citations = doc["citations"]
        url = doc["url"]
        doi = doc["doi"]

        if not title:
            raise ValueError("El documento no tiene título; no se puede insertar.")

        if doi:
            # Upsert por DOI (índice único parcial en tu esquema)
            cur.execute("""
                INSERT INTO oogsj_data.document (title, year, venue, citations, url, doi)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (doi) WHERE doi IS NOT NULL DO UPDATE
                SET
                  title = COALESCE(EXCLUDED.title, oogsj_data.document.title),
                  year = COALESCE(EXCLUDED.year, oogsj_data.document.year),
                  venue = COALESCE(EXCLUDED.venue, oogsj_data.document.venue),
                  citations = COALESCE(EXCLUDED.citations, oogsj_data.document.citations),
                  url = COALESCE(EXCLUDED.url, oogsj_data.document.url)
                RETURNING id, (xmax = 0) AS inserted
            """, (title, year, venue, citations, url, doi))
            rid, inserted = cur.fetchone()
            return rid, bool(inserted)

        # Sin DOI: buscar existente por heurística
        first_author = doc["authors"][0] if doc["authors"] else None
        existing_id = ScientificDocScraper._find_document_without_doi(cur, title, year, first_author)
        if existing_id:
            # Actualizar de forma conservadora (solo si vienen valores no nulos)
            cur.execute("""
                UPDATE oogsj_data.document
                SET
                  venue = COALESCE(%s, venue),
                  citations = COALESCE(%s, citations),
                  url = COALESCE(%s, url)
                WHERE id = %s
                RETURNING id
            """, (venue, citations, url, existing_id))
            rid = cur.fetchone()[0]
            return rid, False

        # Insert nuevo
        cur.execute("""
            INSERT INTO oogsj_data.document (title, year, venue, citations, url, doi)
            VALUES (%s, %s, %s, %s, %s, NULL)
            RETURNING id
        """, (title, year, venue, citations, url))
        rid = cur.fetchone()[0]
        return rid, True

    @staticmethod
    def _link_authors(cur, document_id: int, authors: List[str]):
        """Crea filas en document_author respetando el orden; ignora si ya existen."""
        order = 1
        for full_name in authors:
            author_id = ScientificDocScraper._ensure_author(cur, full_name)
            # Evitar duplicado (PK compuesta y UNIQUE por order)
            cur.execute("""
                INSERT INTO oogsj_data.document_author (document_id, author_id, author_order)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (document_id, author_id, order))
            order += 1

    @staticmethod
    def _insert_source(cur, document_id: int, payload: Dict, source_name: str = "openalex"):
        cur.execute("""
            INSERT INTO oogsj_data.document_source (document_id, source_type, uploaded_by, source_name, raw_payload)
            VALUES (%s, 'scraper', NULL, %s, %s)
        """, (document_id, source_name, Json(payload)))

    # --------------------------
    # Punto de entrada para Celery
    # --------------------------
    @staticmethod
    def fetch_data():
        """
        Método que Celery llamará. Corre todas las queries configuradas,
        pagina resultados y hace la ingesta completa en la BD.
        """
        db = DBHandler()
        if not db.conn or not db.cur:
            logging.error("No hay conexión a BD. Abortando.")
            return {"found": 0, "inserted": 0, "updated": 0, "skipped": 0, "errors": 1}

        found = inserted = updated = skipped = errors = 0

        try:
            for q in QUERIES:
                logging.info(f"🔎 Buscando en OpenAlex: {q}")
                for raw in ScientificDocScraper._iter_openalex_results(q):
                    found += 1
                    doc = ScientificDocScraper._extract_fields(raw)

                    # Validaciones mínimas
                    if not doc["title"]:
                        skipped += 1
                        continue

                    # Transacción por documento
                    try:
                        # BEGIN implícito
                        rid, created = ScientificDocScraper._upsert_document(db.cur, doc)
                        if created:
                            inserted += 1
                        else:
                            updated += 1

                        ScientificDocScraper._link_authors(db.cur, rid, doc["authors"] or [])
                        ScientificDocScraper._insert_source(db.cur, rid, doc["raw"], source_name="openalex")

                        db.conn.commit()
                    except Exception as e:
                        db.conn.rollback()
                        errors += 1
                        logging.exception(f"Error procesando doc '{doc.get('title')}' (DOI={doc.get('doi')}): {e}")
        finally:
            db.close()

        resumen = {"found": found, "inserted": inserted, "updated": updated, "skipped": skipped, "errors": errors}
        logging.info(f"Resumen scraper documentos: {resumen}")
        print(f"Resumen scraper documentos: {resumen}")
        return resumen
