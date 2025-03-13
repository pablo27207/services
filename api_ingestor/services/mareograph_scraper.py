import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MareographScraper:
    URL = "http://tidesud.com/Data/Data_Comodoro%20Rivadavia_Comodoro%20Rivadavia.html"

    @staticmethod
    def fetch_mareograph_data():
        response = requests.get(MareographScraper.URL)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", class_="dataframe")
        rows = table.find_all("tr")[1:]  # Saltar la cabecera

        datos = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 2:
                continue  # Saltar filas inválidas

            date_time = datetime.strptime(cols[0].text, "%d/%m/%y %H:%M")  # Formato: 09/03/25 23:40
            level = float(cols[1].text)  # 4.01

            datos.append((
                date_time,  # timestamp
                level,  # value
                2,  # quality_flag (probablemente bueno)
                1,  # processing_level_id (Raw)
                1,  # sensor_id 1 Mareógrafo - Puerto Comodoro Rivadavia
                1  # location_id puerto de comodoro rivadavia
            ))
        return datos
