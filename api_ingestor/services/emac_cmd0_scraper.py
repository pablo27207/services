"""
emac_cmd0_scraper.py
====================
Scraper para la estación hidrometeorológica CMD0 del sistema EMAC/CRIBA,
ubicada en Caleta Córdova (-45.749189, -67.368762).

Patrón idéntico al de BuoyScraper (misma fuente EMAC, mismo formato CSV).

Variables que obtiene (últimos 30 días de cada endpoint):
  var_code=16 → Nivel del Agua           (m)
  var_code=13 → Temperatura del Agua     (°C)
  var_code=17 → Conductividad            (mS/cm)
  var_code=05 → Temperatura del Aire     (°C)
  var_code=03 → Velocidad del Viento     (km/h en API → m/s almacenado)
  var_code=02 → Dirección del Viento     (°)

IDs de sensor esperados tras aplicar la migración
20260601_add_emac_cmd0_station.sql sobre una BD limpia (init.sql):
  78 → Nivel del Agua
  79 → Temperatura del Agua
  80 → Conductividad
  81 → Temperatura del Aire
  82 → Velocidad del Viento
  83 → Dirección del Viento

Si los IDs reales difieren (p.ej. porque se insertaron otros sensores antes),
ejecutar la consulta de verificación que figura al final de la migración y
actualizar el diccionario VARIABLES a continuación.
"""

import requests
import pandas as pd
import io
from datetime import datetime


# ── Constante de conversión de unidades ────────────────────────────────────
_KMH_TO_MS = 1.0 / 3.6   # 1 km/h = 0.2778 m/s


class EMACCMD0Scraper:
    """
    Scraper de histórico (30 días) de la estación EMAC CMD0 - Caleta Córdova.
    Retorna una lista de tuplas listas para insertar en oogsj_data.measurement.
    """

    # URL base del servicio de históricos EMAC
    BASE_URL = "http://emac.criba.edu.ar/servicios/getHistoryValues.php"

    # Código de estación en el sistema EMAC
    STATION_CODE = "CMD0"

    # Mapeo: var_code → (sensor_id, función de conversión o None)
    #   - Los sensor_id corresponden a la migración 20260601_add_emac_cmd0_station.sql.
    #   - La función de conversión se aplica sobre el valor crudo antes de guardar.
    VARIABLES = {
        "16": (78, None),                    # Nivel del Agua (m) — sin conversión
        "13": (79, None),                    # Temperatura del Agua (°C) — sin conversión
        "17": (80, None),                    # Conductividad (mS/cm) — sin conversión
        "05": (81, None),                    # Temperatura del Aire (°C) — sin conversión
        "03": (82, lambda v: v * _KMH_TO_MS),  # Vel. Viento km/h → m/s
        "02": (83, None),                    # Dirección del Viento (°) — sin conversión
    }

    # ID de la ubicación en platform_location_history (entrada creada en la migración)
    LOCATION_ID = 5

    # Calidad 1 = "Bueno" (datos sin QC adicional; la fuente EMAC ya aplica QC básico)
    QUALITY_FLAG = 1

    # Nivel 1 = "Raw" (datos crudos del sensor; sin reprocesamiento adicional)
    PROCESSING_LEVEL_ID = 1

    @staticmethod
    def fetch_station_data():
        """
        Consulta el histórico de 30 días de cada variable en la API EMAC/CRIBA,
        parsea el CSV que devuelve, aplica conversiones de unidades donde corresponde
        y retorna una lista de tuplas con el formato esperado por DBHandler.insert_measurements().

        Formato de cada tupla:
            (timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)

        Manejo de errores:
            - Error HTTP: se logea y se continúa con la siguiente variable.
            - Respuesta vacía o mal formada: se logea y se continúa.
            - Valor NaN después de parseo: se descarta la fila.
        """
        results = []

        for var_code, (sensor_id, convert_fn) in EMACCMD0Scraper.VARIABLES.items():

            # Construir URL para esta variable
            url = (
                f"{EMACCMD0Scraper.BASE_URL}"
                f"?station_code={EMACCMD0Scraper.STATION_CODE}"
                f"&var_code={var_code}"
            )

            try:
                # ── Petición HTTP ────────────────────────────────────────────
                response = requests.get(url, timeout=15)
                response.raise_for_status()  # Lanza excepción en 4xx/5xx

                # Verificar que la respuesta tenga contenido
                if not response.text.strip():
                    raise ValueError("La API devolvió una respuesta vacía")

                # ── Parseo del CSV ───────────────────────────────────────────
                # El servicio EMAC retorna dos columnas sin encabezado explícito:
                #   columna 0 → timestamp ISO o similar
                #   columna 1 → valor numérico de la variable
                df = pd.read_csv(io.StringIO(response.text), header=0)

                # Validar que el CSV tiene al menos 2 columnas
                if df.shape[1] < 2:
                    raise ValueError(
                        f"Formato CSV inesperado: se esperaban ≥2 columnas, "
                        f"se encontraron {df.shape[1]}"
                    )

                # Renombrar columnas a nombres canónicos
                df.columns = ["timestamp", "value"] + list(df.columns[2:])

                # Parsear timestamp; filas con formato inválido → NaT → se descartan
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

                # Parsear valor numérico; texto no numérico → NaN → se descarta
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

                # Descartar filas con timestamp o valor inválido
                df = df.dropna(subset=["timestamp", "value"])

                if df.empty:
                    print(
                        f"[CMD0][WARN] var_code={var_code} sensor_id={sensor_id}: "
                        f"sin datos válidos tras parseo"
                    )
                    continue

                # ── Conversión de unidades (si aplica) ──────────────────────
                # Solo var_code=03 (viento en km/h) necesita conversión a m/s.
                if convert_fn is not None:
                    df["value"] = df["value"].apply(convert_fn)

                # ── Construcción de tuplas para inserción ────────────────────
                # Formato: (timestamp, value, quality_flag, processing_level_id,
                #           sensor_id, location_id)
                tuples = [
                    (
                        row["timestamp"],
                        float(row["value"]),
                        EMACCMD0Scraper.QUALITY_FLAG,
                        EMACCMD0Scraper.PROCESSING_LEVEL_ID,
                        sensor_id,
                        EMACCMD0Scraper.LOCATION_ID,
                    )
                    for _, row in df.iterrows()
                ]
                results.extend(tuples)

                print(
                    f"[CMD0][OK] var_code={var_code} sensor_id={sensor_id}: "
                    f"{len(tuples)} registros obtenidos"
                )

            except requests.exceptions.Timeout:
                # El servidor EMAC no respondió en 15 segundos
                print(f"[CMD0][ERROR HTTP] var_code={var_code} sensor_id={sensor_id}: timeout")

            except requests.exceptions.HTTPError as e:
                # La API respondió con un código de error HTTP
                print(f"[CMD0][ERROR HTTP] var_code={var_code} sensor_id={sensor_id}: {e}")

            except requests.exceptions.RequestException as e:
                # Error de red genérico (DNS, conexión rechazada, etc.)
                print(f"[CMD0][ERROR RED] var_code={var_code} sensor_id={sensor_id}: {e}")

            except ValueError as e:
                # Datos mal formados o respuesta vacía
                print(f"[CMD0][ERROR DATOS] var_code={var_code} sensor_id={sensor_id}: {e}")

            except Exception as e:
                # Cualquier otro error inesperado no interrumpe el loop
                print(f"[CMD0][ERROR INESPERADO] var_code={var_code} sensor_id={sensor_id}: {e}")

        # Retorno vacío si todas las variables fallaron
        if not results:
            print("[CMD0][WARN] No se obtuvieron datos de ninguna variable.")

        return results
