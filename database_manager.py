# database_manager.py (v1.5 - The Final Blueprint)
import sqlite3, logging
from pathlib import Path

DB_FILE = Path(__file__).parent / "omega_prime.db"
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE); conn.row_factory = sqlite3.Row; return conn
    except sqlite3.Error as e:
        logger.critical(f"FATAL: डाटाबेससँग जडान हुन सकेन: {e}"); return None

def _create_tables(cursor):
    """दरबारको भित्री कोठाहरू (तालिकाहरू) बनाउँछ।"""
    logger.info("    - 'coins', 'signals', 'historical_data' तालिकाहरू बनाउँदै...")
    cursor.execute("CREATE TABLE coins (id INTEGER PRIMARY KEY, symbol TEXT NOT NULL, name TEXT NOT NULL, coingecko_id TEXT UNIQUE, contract_address TEXT UNIQUE, chain TEXT, price_usd REAL, volume_24h REAL, market_cap REAL, last_seen TIMESTAMP);")
    cursor.execute("CREATE TABLE signals (id INTEGER PRIMARY KEY, coin_id INTEGER, timestamp TIMESTAMP, signal_type TEXT, meta_json TEXT, weight REAL, FOREIGN KEY (coin_id) REFERENCES coins (id));")
    cursor.execute("CREATE TABLE historical_data (id INTEGER PRIMARY KEY, coin_id INTEGER, date TEXT, price REAL, UNIQUE(coin_id, date), FOREIGN KEY (coin_id) REFERENCES coins (id));")

def ensure_database_integrity():
    """
    शाही आदेश: यो प्रकार्यले सुनिश्चित गर्छ कि जग अवस्थित छ। यदि छैन भने, यसले आफैं बनाउँछ।
    """
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins';")
        if cursor.fetchone() is None:
            logger.warning("साम्राज्यको जग फेला परेन! महान् पुनर्स्थापना सुरु हुँदैछ...")
            _create_tables(cursor)
            conn.commit()
            logger.info("✅ महान् पुनर्स्थापना सम्पन्न भयो।")
        return True
    except sqlite3.Error as e:
        logger.error(f"डाटाबेस अखण्डता जाँचमा त्रुटि: {e}"); return False
    finally:
        conn.close()
