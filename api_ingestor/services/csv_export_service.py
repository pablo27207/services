from __future__ import annotations

import csv
import os
import re
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime, timedelta

import psycopg2

from services.config import DB_CONFIG

EXPORT_DIR = os.environ.get("EXPORT_DIR", "/app/exports")


def slugify(text: str) -> str:
    text = text.lower()
    for src, dst in [("á","a"),("à","a"),("ä","a"),("â","a"),("ã","a"),
                     ("é","e"),("è","e"),("ë","e"),("ê","e"),
                     ("í","i"),("ì","i"),("ï","i"),("î","i"),
                     ("ó","o"),("ò","o"),("ö","o"),("ô","o"),("õ","o"),
                     ("ú","u"),("ù","u"),("ü","u"),("û","u"),("ñ","n")]:
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


MEASUREMENT_QUERY = """
    SELECT
        m.timestamp,
        v.name                          AS variable,
        u.symbol                        AS unidad,
        m.value                         AS valor,
        COALESCE(m.quality_flag::text, 'N/A')   AS quality_flag,
        COALESCE(qf.description, 'N/A')         AS flag_descripcion,
        COALESCE(pl.level, 'N/A')               AS nivel_procesamiento
    FROM oogsj_data.measurement m
    JOIN oogsj_data.sensor           s  ON m.sensor_id          = s.id
    JOIN oogsj_data.variable         v  ON s.variable_id        = v.id
    JOIN oogsj_data.unit             u  ON s.unit_id            = u.id
    LEFT JOIN oogsj_data.quality_flag   qf ON m.quality_flag    = qf.flag
    LEFT JOIN oogsj_data.processing_level pl ON m.processing_level_id = pl.id
    WHERE s.platform_id = %s
      AND m.timestamp >= %s
      AND m.timestamp <  %s
    ORDER BY m.timestamp, v.name;
"""

CSV_HEADER = ["timestamp", "variable", "unidad", "valor",
              "quality_flag", "flag_descripcion", "nivel_procesamiento"]

# Variables cuya unidad en BD es m/s y deben exportarse como km/h.
_WIND_SPEED_VARS = {"wind speed avg", "wind speed hi", "wind speed", "velocidad del viento"}


def _to_display(variable: str, unit: str, value):
    """Convierte m/s → km/h para variables de velocidad de viento."""
    if unit == "m/s" and variable.strip().lower() in _WIND_SPEED_VARS:
        converted = None if value is None else round(float(value) * 3.6, 2)
        return "km/h", converted
    return unit, value


def _month_range(start_year: int, start_month: int, end_year: int, end_month: int):
    """Yields (year, month) tuples from start to end inclusive."""
    y, m = start_year, start_month
    while (y, m) <= (end_year, end_month):
        yield y, m
        m += 1
        if m > 12:
            m = 1
            y += 1


class CSVExportService:

    @staticmethod
    def _connect():
        return psycopg2.connect(**DB_CONFIG)

    @staticmethod
    def _get_platforms(conn):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, p.name, pt.name
                FROM oogsj_data.platform p
                JOIN oogsj_data.platform_type pt ON p.platform_type_id = pt.id
                ORDER BY p.id;
            """)
            return cur.fetchall()   # [(id, name, type_name), ...]

    @staticmethod
    def generate_for_platform(conn, platform_id: int, platform_name: str,
                              platform_type: str, year: int, month: int) -> str | None:
        """Genera un CSV (formato largo) para una plataforma y mes dados."""
        period_start = datetime(year, month, 1)
        last_day     = monthrange(year, month)[1]
        period_end   = datetime(year, month, last_day) + timedelta(days=1)

        slug   = slugify(platform_name)
        folder = os.path.join(EXPORT_DIR, slug, str(year))
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, f"{year}_{month:02d}_{slug}.csv")

        with conn.cursor() as cur:
            cur.execute(MEASUREMENT_QUERY, (platform_id, period_start, period_end))
            rows = cur.fetchall()

        if not rows:
            print(f"⚠️  Sin datos: {platform_name} {year}-{month:02d}")
            return None

        display_rows = []
        for ts, variable, unit, value, qf, qfd, pl in rows:
            unit_d, value_d = _to_display(variable, unit, value)
            display_rows.append((ts, variable, unit_d, value_d, qf, qfd, pl))

        with open(filepath, "w", newline="", encoding="utf-8") as fh:
            fh.write(f"# Plataforma: {platform_name}\n")
            fh.write(f"# Tipo: {platform_type}\n")
            fh.write(f"# Período: {period_start.strftime('%Y-%m-%d')} / {datetime(year, month, last_day).strftime('%Y-%m-%d')}\n")
            fh.write(f"# Generado: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
            fh.write(f"# Registros: {len(display_rows)}\n")
            writer = csv.writer(fh)
            writer.writerow(CSV_HEADER)
            writer.writerows(display_rows)

        print(f"✅ {filepath}  ({len(rows):,} registros)")
        return filepath

    @staticmethod
    def generate_txt_for_platform(conn, platform_id: int, platform_name: str,
                                  platform_type: str, year: int, month: int) -> str | None:
        """
        Genera un TXT pivotado (formato ancho) para una plataforma y mes dados.
        Cada fila = un timestamp; cada columna = una variable[unidad].
        Separador: TAB. Valores ausentes: NaN.
        """
        period_start = datetime(year, month, 1)
        last_day     = monthrange(year, month)[1]
        period_end   = datetime(year, month, last_day) + timedelta(days=1)

        slug   = slugify(platform_name)
        folder = os.path.join(EXPORT_DIR, slug, str(year))
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, f"{year}_{month:02d}_{slug}.txt")

        with conn.cursor() as cur:
            cur.execute(MEASUREMENT_QUERY, (platform_id, period_start, period_end))
            rows = cur.fetchall()

        if not rows:
            return None

        # Pivot: agrupar por timestamp, variables como columnas
        data: dict[datetime, dict[str, float]] = defaultdict(dict)
        col_order: list[str] = []
        seen_cols: set[str] = set()

        for ts, variable, unit, value, _qf, _qfd, _pl in rows:
            unit_d, value_d = _to_display(variable, unit, value)
            col = f"{variable}[{unit_d}]"
            if col not in seen_cols:
                col_order.append(col)
                seen_cols.add(col)
            data[ts][col] = value_d

        all_timestamps = sorted(data.keys())

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(f"# Plataforma: {platform_name}\n")
            fh.write(f"# Tipo: {platform_type}\n")
            fh.write(f"# Periodo: {period_start.strftime('%Y-%m-%d')} / {datetime(year, month, last_day).strftime('%Y-%m-%d')}\n")
            fh.write(f"# Generado: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
            fh.write(f"# Timestamps: {len(all_timestamps)}  Variables: {len(col_order)}\n")
            fh.write("# Separador: TAB  |  Valor ausente: NaN\n")
            fh.write("\t".join(["timestamp"] + col_order) + "\n")
            for ts in all_timestamps:
                row_vals = [str(data[ts].get(col, "NaN")) for col in col_order]
                fh.write(str(ts) + "\t" + "\t".join(row_vals) + "\n")

        print(f"✅ {filepath}  ({len(all_timestamps):,} timestamps, {len(col_order)} variables)")
        return filepath

    @staticmethod
    def generate_all_platforms(year: int = None, month: int = None) -> list[str]:
        """
        Genera CSV y TXT por plataforma para el mes indicado.
        Si no se pasa año/mes, usa el mes anterior al día de hoy.
        """
        if year is None or month is None:
            today = date.today()
            if today.month == 1:
                year, month = today.year - 1, 12
            else:
                year, month = today.year, today.month - 1

        print(f"📦 Exportación mensual iniciada: {year}-{month:02d}")

        conn = CSVExportService._connect()
        try:
            platforms = CSVExportService._get_platforms(conn)
            generated = []
            for pid, pname, ptype in platforms:
                try:
                    for gen_fn in (CSVExportService.generate_for_platform,
                                   CSVExportService.generate_txt_for_platform):
                        path = gen_fn(conn, pid, pname, ptype, year, month)
                        if path:
                            generated.append(path)
                except Exception as exc:
                    print(f"❌ Error en '{pname}': {exc}")
            print(f"📦 Exportación completa: {len(generated)}/{len(platforms) * 2} archivos generados")
            return generated
        finally:
            conn.close()

    @staticmethod
    def backfill_all_months(start_year: int = None, start_month: int = None) -> list[str]:
        """
        Genera CSV y TXT para TODAS las plataformas desde el inicio de los datos hasta
        el mes anterior al día de hoy. Útil para poblar el historial completo.
        """
        conn = CSVExportService._connect()
        try:
            if start_year is None:
                with conn.cursor() as cur:
                    cur.execute("SELECT MIN(timestamp) FROM oogsj_data.measurement")
                    min_ts = cur.fetchone()[0]
                if min_ts:
                    start_year, start_month = min_ts.year, min_ts.month
                else:
                    print("⚠️  No hay mediciones en la base de datos.")
                    return []

            today = date.today()
            end_year  = today.year  if today.month > 1 else today.year - 1
            end_month = today.month - 1 if today.month > 1 else 12

            platforms  = CSVExportService._get_platforms(conn)
            generated  = []
            total_months = sum(1 for _ in _month_range(start_year, start_month, end_year, end_month))

            print(f"🗂️  Backfill: {start_year}-{start_month:02d} → {end_year}-{end_month:02d}  "
                  f"({total_months} meses × {len(platforms)} plataformas)")

            for year, month in _month_range(start_year, start_month, end_year, end_month):
                print(f"📅 Procesando {year}-{month:02d} ...")
                for pid, pname, ptype in platforms:
                    try:
                        for gen_fn in (CSVExportService.generate_for_platform,
                                       CSVExportService.generate_txt_for_platform):
                            path = gen_fn(conn, pid, pname, ptype, year, month)
                            if path:
                                generated.append(path)
                    except Exception as exc:
                        print(f"❌ Error en '{pname}' {year}-{month:02d}: {exc}")

            print(f"🏁 Backfill completo: {len(generated)} archivos generados")
            return generated
        finally:
            conn.close()

    @staticmethod
    def generate_platform_by_name(platform_name: str, year: int, month: int) -> str | None:
        """Genera CSV y TXT para una plataforma específica por nombre exacto."""
        conn = CSVExportService._connect()
        try:
            platforms = CSVExportService._get_platforms(conn)
            match = next((p for p in platforms if p[1] == platform_name), None)
            if not match:
                print(f"❌ Plataforma no encontrada: '{platform_name}'")
                return None
            pid, pname, ptype = match
            csv_path = CSVExportService.generate_for_platform(conn, pid, pname, ptype, year, month)
            txt_path = CSVExportService.generate_txt_for_platform(conn, pid, pname, ptype, year, month)
            return csv_path or txt_path
        finally:
            conn.close()
