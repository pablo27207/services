import logging
import psycopg2
from psycopg2.extras import execute_values
from .config import DB_CONFIG

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DBHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor()
            logger.info("✅ Conexión a PostgreSQL establecida.")
        except Exception as e:
            logger.error(f"🚨 Error al conectar a PostgreSQL: {e}", exc_info=True)

    def insert_measurements(self, data):
        try:
            query = """
            INSERT INTO oogsj_data.measurement (timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)
            VALUES %s
            ON CONFLICT DO NOTHING;
            """
            execute_values(self.cur, query, data)
            self.conn.commit()
            logging.info(f"✅ {len(data)} registros insertados correctamente.")
        except Exception as e:
            logging.error(f"⚠️ Error al insertar datos en la base de datos: {e}", exc_info=True)



    def close(self):
        self.cur.close()
        self.conn.close()
        logger.info("🔌 Conexión a la base de datos cerrada.")
