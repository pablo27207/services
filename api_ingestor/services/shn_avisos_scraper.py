import time
import requests
from datetime import datetime

BASE_URL  = "https://geoportal.shn.gob.ar/api/v1"
VIGENTES  = f"{BASE_URL}/Radioavisos/Geoportal/Vigentes"
DETALLE   = f"{BASE_URL}/Radioavisos/{{id}}"

ESTACIONES_OBJETIVO = {
    "NAVTEX COMODORO RIVADAVIA",
    "NAVTEX RIO GALLEGOS",
}

KEYWORDS = [
    "golfo san jorge", "chubut", "comodoro", "rawson",
    "caleta córdova", "caleta cordova", "camarones",
    "deseado", "comodoro rivadavia", "santa cruz",
    "golfo nuevo", "golfo san josé", "puerto madryn",
    "punta ninfas", "isla rasa", "cabo guardian",
    "cabo dañoso", "cabo curioso", "isla pingüino",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://geoportal.shn.gob.ar/",
    "Accept":  "application/json",
}


def _es_relevante(texto_es, texto_en):
    combined = f"{texto_es or ''} {texto_en or ''}".lower()
    return any(kw in combined for kw in KEYWORDS)


def _parse_fecha(fecha_str):
    if not fecha_str:
        return None
    try:
        return datetime.fromisoformat(fecha_str[:19]).date()
    except Exception:
        return None


class SHNAvisosScraper:

    @staticmethod
    def fetch_avisos_data():
        try:
            resp = requests.get(VIGENTES, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"❌ SHN Vigentes error: {e}")
            return []

        ids_objetivo = []
        for grupo in data.get("avisos", []):
            descripcion = (grupo.get("descripcion") or "").upper()
            if any(est in descripcion for est in ESTACIONES_OBJETIVO):
                for child in grupo.get("children", []):
                    aviso_id = child.get("id")
                    if aviso_id and aviso_id > 0:
                        ids_objetivo.append(aviso_id)

        print(f"📡 SHN: {len(ids_objetivo)} avisos en estaciones objetivo")

        resultados = []
        for aviso_id in ids_objetivo:
            try:
                url  = DETALLE.format(id=aviso_id)
                resp = requests.get(url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                av   = resp.json()

                numero   = av.get("numero", "").strip()
                fecha_s  = av.get("fecha", "")
                tipo     = av.get("tipoAviso", "").strip()
                texto_es = (av.get("textoEsp") or "").strip()
                texto_en = (av.get("textoIng") or "").strip()

                if not numero:
                    time.sleep(1)
                    continue

                fecha = _parse_fecha(fecha_s)
                if not fecha:
                    time.sleep(1)
                    continue

                if not _es_relevante(texto_es, texto_en):
                    print(f"  ↩ {numero} — no relevante para la región")
                    time.sleep(1)
                    continue

                resultados.append((numero, fecha, tipo, texto_es, texto_en))
                print(f"  ✅ {numero} — {tipo}")
                time.sleep(1)

            except Exception as e:
                print(f"  ⚠️ Error obteniendo aviso {aviso_id}: {e}")
                time.sleep(2)  # más espera si hubo error (429)
                continue

        print(f"📋 SHN: {len(resultados)} avisos relevantes para Chubut/GSJ")
        return resultados