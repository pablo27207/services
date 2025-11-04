import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class ScientificDocScraper:
    """Clase para extraer datos de documentos científicos de una página de resultados."""

    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_and_parse(self, query: str) -> List[Dict]:
        """
        Realiza la búsqueda y procesa el HTML.
        
        NOTA: La URL final y los parámetros de la query (q, page)
        dependerán de cómo el sitio web construye sus URLs de búsqueda.
        """
        search_url = f"{self.base_url}?q={query.replace(' ', '+')}"
        
        try:
            response = requests.get(search_url, timeout=15)
            response.raise_for_status() # Lanza error para códigos 4xx/5xx
        except requests.RequestException as e:
            print(f"Error al acceder a la URL: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 1. ENCONTRAR TODOS LOS 'ITEMS' DE RESULTADO
        # Esto localiza el contenedor de cada documento (ej. un div con clase 'result-item')
        result_items = soup.find_all("div", class_="contenedor-de-resultado") # Reemplazar por el selector real

        documentos = []
        for item in result_items:
            data = self._extract_item_data(item)
            if data:
                documentos.append(data)
                
        return documentos

    def _extract_item_data(self, item_tag) -> Dict | None:
        """
        Extrae los campos individuales de un único elemento de resultado.
        """
        # --- EXTRACCIÓN DEL TÍTULO ---
        # El título está en un <h3> o <a> con una clase específica
        title_tag = item_tag.find("h3", class_="titulo-del-documento") # SELECTOR
        title = title_tag.text.strip() if title_tag else "(Sin Título)"

        # --- EXTRACCIÓN DE METADATOS (Año, Venue, Citas) ---
        # Estos suelen estar cerca en un <div> o <p>
        meta_area = item_tag.find("div", class_="metadata-linea") # SELECTOR para la línea que contiene Año, Citas, Venue
        
        year = None
        venue = None
        citations = 0
        
        if meta_area:
            # Ejemplo para el año (asume que el año tiene un span con clase 'year-tag')
            year_tag = meta_area.find("span", class_="year-tag")
            if year_tag:
                try:
                    year = int(year_tag.text.strip())
                except ValueError:
                    pass # Deja 'year' como None si falla la conversión

            # Ejemplo para el Venue (asume que el venue es el texto dentro de un span con clase 'venue-tag')
            venue_tag = meta_area.find("span", class_="venue-tag")
            venue = venue_tag.text.strip() if venue_tag else "(Desconocido)"

            # Ejemplo para Citas (asume un span que contiene 'Citas: X')
            citations_tag = meta_area.find("span", string=lambda t: t and "Citas:" in t)
            if citations_tag:
                try:
                    # Extraer el número después de 'Citas:'
                    citations_str = citations_tag.text.split(':')[1].strip()
                    citations = int(citations_str)
                except (IndexError, ValueError):
                    pass # Deja 'citations' como 0 si falla

        # --- EXTRACCIÓN DE URL y DOI ---
        # El botón 'Ver fuente' (URL) y 'DOI' (si existe)
        url = None
        doi = None

        # Enlace a la fuente (generalmente el href del botón 'Ver fuente')
        source_link = item_tag.find("a", string="Ver fuente") # SELECTOR o ajusta para buscar el link
        if source_link and 'href' in source_link.attrs:
            url = source_link['href']

        # Enlace del DOI (puede ser el href del botón 'DOI')
        doi_link = item_tag.find("a", string="DOI") # SELECTOR
        if doi_link and 'href' in doi_link.attrs:
            doi = doi_link['href'].split("doi.org/")[-1] # Simplificado: extrae solo el identificador

        # --- EXTRACCIÓN DE AUTORES ---
        # Esto es crucial y no se ve en tu imagen. Asume que hay un div o p con la lista de autores.
        author_list_tag = item_tag.find("div", class_="author-list") # SELECTOR
        authors = []
        if author_list_tag:
            # Asume que los nombres están en <a> tags dentro de author_list_tag
            authors = [a.text.strip() for a in author_list_tag.find_all("a")]
        
        # Si el título es nulo o inválido, podrías retornar None o seguir con el default.
        if title == "(Sin Título)":
             return None 

        return {
            "title": title,
            "year": year,
            "venue": venue,
            "citations": citations,
            "author": authors, # Lo necesitarás para la segunda parte de tu script SQL
            "url": url,
            "doi": doi
        }

# --- EJEMPLO DE USO ---
# scraper = ScientificDocScraper("http://ejemplo-sitio-cientifico.org/search")
# resultados = scraper.fetch_and_parse("Golfo San Jorge Argentina")
# print(resultados)