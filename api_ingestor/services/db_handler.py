import logging
import psycopg2
from psycopg2.extras import execute_values
from .config import DB_CONFIG
from datetime import datetime

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

    def insert_mareograph_data(self, data):
        try:
            query = "INSERT INTO mareograph_data (timestamp, level) VALUES %s ON CONFLICT DO NOTHING;"
            execute_values(self.cur, query, data)
            self.conn.commit()
            logger.info("✅ %d registros insertados en mareograph_data.", len(data))
        except Exception as e:
            logger.error(f"⚠️ Error al insertar en la base de datos: {e}", exc_info=True)

    def insert_tide_forecast(self, data):
        try:
            query = "INSERT INTO tide_forecast (timestamp, level) VALUES %s ON CONFLICT DO NOTHING;"
            execute_values(self.cur, query, data)
            self.conn.commit()
            logger.info("✅ %d registros insertados en tide_forecast.", len(data))
        except Exception as e:
            logger.error(f"⚠️ Error al insertar en la base de datos: {e}", exc_info=True)

    def insert_buoy_data(self, data):
        try:
            logger.info(f"✅ Insertando {len(data)} registros en la tabla buoy_data...")
            query = "INSERT INTO buoy_data (timestamp, variable, value) VALUES %s ON CONFLICT DO NOTHING;"
            execute_values(self.cur, query, data)
            self.conn.commit()
            logger.info("✅ %d registros insertados en buoy_data.", len(data))
        except Exception as e:
            logger.error(f"⚠️ Error al insertar datos de la boya: {e}", exc_info=True)


    def close(self):
        self.cur.close()
        self.conn.close()
        logger.info("🔌 Conexión a la base de datos cerrada.")