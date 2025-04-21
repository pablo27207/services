import psycopg2
from psycopg2.extras import execute_values
from .config import DB_CONFIG

class DBHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor()
            print("✅ Conexión a PostgreSQL establecida.")
        except Exception as e:
            print(f"🚨 Error al conectar a PostgreSQL: {e}")
            self.conn = None
            self.cur = None

    def insert_measurements(self, data):
        if not self.conn or not self.cur:
            print("⚠️ No se puede insertar datos porque la conexión no está activa.")
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
            print(f"✅ {len(data)} registros insertados correctamente.")
        except Exception as e:
            print(f"⚠️ Error al insertar datos en la base de datos: {e}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("🔌 Conexión a la base de datos cerrada.")
