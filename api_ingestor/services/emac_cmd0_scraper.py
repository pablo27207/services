"""
emac_cmd0_scraper.py
====================
Scraper para la estación hidrometeorológica CMD0 del sistema EMAC/CRIBA,
ubicada en Caleta Córdova (-45.749189, -67.368762).

Variables que obtiene (últimos 30 días de cada endpoint):
  var_code=16 → Nivel del Agua           (m)
  var_code=13 → Temperatura del Agua     (°C)
  var_code=17 → Conductividad            (mS/cm)
  var_code=05 → Temperatura del Aire     (°C)
  var_code=03 → Velocidad del Viento     (km/h en API → m/s almacenado)
  var_code=02 → Dirección del Viento     (°)

Los sensor_id y location_id se resuelven dinámicamente desde la BD al
momento de la ejecución, por lo que son independientes del entorno
(desarrollo, producción, etc.).
"""

import io

import psycopg2
import requests
import pandas as pd

from .config import DB_CONFIG


_KMH_TO_MS = 1.0 / 3.6

# Mapeo: nombre del sensor (contenido en s.name) → (var_code, conversion_fn)
_SENSOR_MAP = {
    "Sensor de Nivel del Agua - CMD0":         ("16", None),
    "Sensor de Temperatura del Agua - CMD0":   ("13", None),
    "Sensor de Conductividad - CMD0":          ("17", None),
    "Sensor de Temperatura del Aire - CMD0":   ("05", None),
    "Sensor de Velocidad del Viento - CMD0":   ("03", lambda v: v * _KMH_TO_MS),
    "Sensor de Dirección del Viento - CMD0":   ("02", None),
}

_PLATFORM_NAME = "Estación EMAC - Caleta Córdova CMD0"


def _resolve_ids():
    """
    Consulta la BD y devuelve:
      variables   → {var_code: (sensor_id, convert_fn)}
      location_id → int

    Lanza RuntimeError si la plataforma no existe o no tiene sensores.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT s.name, s.id
            FROM oogsj_data.sensor s
            JOIN oogsj_data.platform p ON p.id = s.platform_id
            WHERE p.name = %s
        """, (_PLATFORM_NAME,))
        sensor_rows = cur.fetchall()

        if not sensor_rows:
            raise RuntimeError(
                f"[CMD0] No se encontraron sensores para '{_PLATFORM_NAME}'. "
                "Verificar que la migración 20260601_add_emac_cmd0_station.sql fue aplicada."
            )

        variables = {}
        for sensor_name, sensor_id in sensor_rows:
            if sensor_name in _SENSOR_MAP:
                var_code, convert_fn = _SENSOR_MAP[sensor_name]
                variables[var_code] = (sensor_id, convert_fn)

        cur.execute("""
            SELECT plh.id
            FROM oogsj_data.platform_location_history plh
            JOIN oogsj_data.platform p ON p.id = plh.platform_id
            WHERE p.name = %s AND plh.end_time IS NULL
            ORDER BY plh.start_time DESC
            LIMIT 1
        """, (_PLATFORM_NAME,))
        row = cur.fetchone()
        if not row:
            raise RuntimeError(f"[CMD0] No se encontró location activa para '{_PLATFORM_NAME}'.")
        location_id = row[0]

    finally:
        cur.close()
        conn.close()

    return variables, location_id


class EMACCMD0Scraper:
    """
    Scraper de histórico (30 días) de la estación EMAC CMD0 - Caleta Córdova.
    Retorna una lista de tuplas listas para insertar en oogsj_data.measurement.
    """

    BASE_URL    = "http://emac.criba.edu.ar/servicios/getHistoryValues.php"
    STATION_CODE = "CMD0"
    QUALITY_FLAG        = 1
    PROCESSING_LEVEL_ID = 1

    @staticmethod
    def fetch_station_data():
        """
        Resuelve sensor IDs y location_id desde la BD, luego consulta la API
        EMAC/CRIBA por cada variable y retorna las tuplas para inserción.

        Formato de cada tupla:
            (timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)
        """
        try:
            variables, location_id = _resolve_ids()
        except Exception as e:
            print(f"[CMD0][ERROR BD] No se pudieron resolver IDs: {e}")
            return []

        results = []

        for var_code, (sensor_id, convert_fn) in variables.items():
            url = (
                f"{EMACCMD0Scraper.BASE_URL}"
                f"?station_code={EMACCMD0Scraper.STATION_CODE}"
                f"&var_code={var_code}"
            )
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()

                if not response.text.strip():
                    raise ValueError("La API devolvió una respuesta vacía")

                df = pd.read_csv(io.StringIO(response.text), header=0)

                if df.shape[1] < 2:
                    raise ValueError(
                        f"Formato CSV inesperado: se esperaban ≥2 columnas, "
                        f"se encontraron {df.shape[1]}"
                    )

                df.columns = ["timestamp", "value"] + list(df.columns[2:])
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df["value"]     = pd.to_numeric(df["value"], errors="coerce")
                df = df.dropna(subset=["timestamp", "value"])

                if df.empty:
                    print(f"[CMD0][WARN] var_code={var_code} sensor_id={sensor_id}: sin datos válidos tras parseo")
                    continue

                if convert_fn is not None:
                    df["value"] = df["value"].apply(convert_fn)

                tuples = [
                    (
                        row["timestamp"],
                        float(row["value"]),
                        EMACCMD0Scraper.QUALITY_FLAG,
                        EMACCMD0Scraper.PROCESSING_LEVEL_ID,
                        sensor_id,
                        location_id,
                    )
                    for _, row in df.iterrows()
                ]
                results.extend(tuples)
                print(f"[CMD0][OK] var_code={var_code} sensor_id={sensor_id}: {len(tuples)} registros obtenidos")

            except requests.exceptions.Timeout:
                print(f"[CMD0][ERROR HTTP] var_code={var_code} sensor_id={sensor_id}: timeout")
            except requests.exceptions.HTTPError as e:
                print(f"[CMD0][ERROR HTTP] var_code={var_code} sensor_id={sensor_id}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"[CMD0][ERROR RED] var_code={var_code} sensor_id={sensor_id}: {e}")
            except ValueError as e:
                print(f"[CMD0][ERROR DATOS] var_code={var_code} sensor_id={sensor_id}: {e}")
            except Exception as e:
                print(f"[CMD0][ERROR INESPERADO] var_code={var_code} sensor_id={sensor_id}: {e}")

        if not results:
            print("[CMD0][WARN] No se obtuvieron datos de ninguna variable.")

        return results
