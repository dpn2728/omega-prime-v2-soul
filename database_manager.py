# database_manager.py (v1.4 - The Imperial Decree)
import sqlite3
import logging
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
    logger.info("    - 'coins' तालिका बनाउँदै...")
    cursor.execute("""
    CREATE TABLE coins (
        id INTEGER PRIMARY KEY, symbol TEXT NOT NULL, name TEXT NOT NULL,
        coingecko_id TEXT UNIQUE, contract_address TEXT UNIQUE, chain TEXT,
        price_usd REAL DEFAULT 0, volume_24h REAL DEFAULT 0, market_cap REAL DEFAULT 0,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    logger.info("    - 'signals' तालिका बनाउँदै...")
    cursor.execute("""
    CREATE TABLE signals (
        id INTEGER PRIMARY KEY, coin_id INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        signal_type TEXT NOT NULL, meta_json TEXT, weight REAL,
        FOREIGN KEY (coin_id) REFERENCES coins (id)
    );
    """)

def ensure_database_integrity():
    """
    शाही आदेश: यो प्रकार्यले सुनिश्चित गर्छ कि जग अवस्थित छ।
    यदि छैन भने, यसले आफैं बनाउँछ।
    """
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        # 'coins' तालिका छ कि छैन भनेर जाँच गर्ने प्रयास गर्ने
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins';")
        if cursor.fetchone() is None:
            # तालिका अवस्थित छैन, त्यसैले जग निर्माण सुरु गर्ने
            logger.warning("साम्राज्यको जग फेला परेन! महान् पुनर्स्थापना सुरु हुँदैछ...")
            _create_tables(cursor)
            conn.commit()
            logger.info("✅ महान् पुनर्स्थापना सम्पन्न भयो। साम्राज्यको जग अब अटूट छ।")
        else:
            logger.debug("साम्राज्यको जग मान्य छ।")
        return True
    except sqlite3.Error as e:
        logger.error(f"डाटाबेस अखण्डता जाँचमा त्रुटि: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # यो फाइल सीधै चलाउँदा पनि जग बसाल्ने
    ensure_database_integrity()
