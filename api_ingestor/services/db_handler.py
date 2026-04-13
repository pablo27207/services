import psycopg2
from psycopg2.extras import execute_values
from .config import DB_CONFIG


class DBHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur  = self.conn.cursor()
            print("✅ Conexión a PostgreSQL establecida.")
        except Exception as e:
            print(f"🚨 Error al conectar a PostgreSQL: {e}")
            self.conn = None
            self.cur  = None

    # ── Mediciones (existente, sin cambios) ───────────────────────
    def insert_measurements(self, data):
        if not self.conn or not self.cur:
            print("⚠️ Conexión no activa.")
            return
        try:
            query = """
                INSERT INTO oogsj_data.measurement
                    (timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)
                VALUES %s
                ON CONFLICT DO NOTHING;
            """
            execute_values(self.cur, query, data)
            self.conn.commit()
            print(f"✅ {len(data)} registros insertados.")
        except Exception as e:
            print(f"⚠️ Error al insertar mediciones: {e}")

    # ── Avisos del navegante (nuevo) ──────────────────────────────
    def insert_avisos(self, data: list[tuple]):
        """
        Inserta avisos del navegante.
        Cada tupla: (numero, fecha, tipo, texto_es, texto_en)
        ON CONFLICT (numero) actualiza el texto y scraped_at.
        """
        if not self.conn or not self.cur:
            print("⚠️ Conexión no activa.")
            return
        if not data:
            print("⚠️ Sin avisos para insertar.")
            return
        try:
            query = """
                INSERT INTO oogsj_data.aviso_navegante
                    (numero, fecha, tipo, texto_es, texto_en)
                VALUES %s
                ON CONFLICT (numero) DO UPDATE SET
                    texto_es   = EXCLUDED.texto_es,
                    texto_en   = EXCLUDED.texto_en,
                    tipo       = EXCLUDED.tipo,
                    scraped_at = NOW();
            """
            execute_values(self.cur, query, data)
            self.conn.commit()
            print(f"✅ {len(data)} avisos insertados/actualizados.")
        except Exception as e:
            self.conn.rollback()
            print(f"⚠️ Error al insertar avisos: {e}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("🔌 Conexión cerrada.")