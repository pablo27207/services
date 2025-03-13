import requests
from bs4 import BeautifulSoup
from datetime import datetime

class TideScraper:
    BASE_URL = "https://www.hidro.gov.ar/oceanografia/Tmareas/RE_TablasDeMarea.asp"

    SENSOR_ID = 2  # Predicción de Marea - Hidrografía Naval
    LOCATION_ID = 1  # Ubicación: Puerto Comodoro Rivadavia
    PROCESSING_LEVEL_ID = 5  # Model Output
    QUALITY_FLAG = 7  # Estimado
    
    @staticmethod
    def fetch_tide_data():
        headers = {
            "User-Agent": "PostmanRuntime/7.43.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        date = datetime.now()
        year = date.year
        month = date.month

        data = {
            "Fanio": str(year),
            "Localidad": "COMO",
            "Fmes": f"{month:02d}",
            "B1": ""
        }

        try:
            response = requests.post(
                TideScraper.BASE_URL,
                headers=headers,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            table_div = soup.find("div", class_="LetraMasChica")
            if not table_div:
                raise ValueError("No se encontró la tabla en la página")

            table = table_div.find("table")
            if not table:
                raise ValueError("No se encontró la tabla de datos")

            rows = table.find_all("tr")[1:]  # Ignorar la primera fila (encabezados)
            results = []
            last_valid_day = None

            for row in rows:
                columns = row.find_all("td")
                if len(columns) < 3:
                    continue

                dia = columns[0].text.strip()  # Puede estar vacío en filas posteriores
                hora_min = columns[1].text.strip()
                altura = columns[2].text.strip().replace(",", ".")  # Convertimos la coma en punto decimal

                # Si la columna del día no está vacía, actualizar el último día válido
                if dia:
                    last_valid_day = dia.zfill(2)  # Asegurar que tenga dos dígitos (ej: "01", "02")

                if last_valid_day is None:
                    continue

                # Construir la fecha completa
                date_time = f"{last_valid_day}/{month:02d}/{year} {hora_min}"
                date_time = datetime.strptime(date_time, "%d/%m/%Y %H:%M")  # Formato: 09/03/25 23:40

                # Devolver datos en formato ID
                results.append((
                    date_time,  # timestamp
                    float(altura),  # value
                    TideScraper.QUALITY_FLAG,  # quality_flag (Estimado)
                    TideScraper.PROCESSING_LEVEL_ID,  # processing_level_id (Model Output)
                    TideScraper.SENSOR_ID,
                    TideScraper.LOCATION_ID
                ))

            return results

        except requests.RequestException as e:
            print(f"❌ Error al hacer la petición: {e}")
            return []
