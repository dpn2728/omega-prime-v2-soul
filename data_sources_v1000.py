# data_sources_v1000.py (v1.6 - The Corrected Orders)

import requests
import logging
import time
from datetime import datetime, timedelta

# --- समाधान: 'setup_database' को सट्टा 'ensure_database_integrity' लाई बोलाउने ---
from database_manager import get_db_connection, ensure_database_integrity, DB_FILE
from config import MARKET_PARAMETERS

logger = logging.getLogger(__name__)

class WiseLibrarian:
    def __init__(self):
        self.coingecko_api_base = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'OmegaPrime/1000.6'})

    def _fetch_with_governor(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=45)
            if response.status_code == 429:
                logger.warning("दर सीमा पुग्यो। ६० सेकेन्ड पर्खिँदै...")
                time.sleep(61)
                response = self.session.get(url, params=params, timeout=45)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API सँग सञ्चार गर्न असफल: {e}")
        return None
        
    def get_market_pulse(self):
        pulse = {"fear_and_greed": "N/A", "btc_dominance": "N/A"}
        try:
            fng_data = self._fetch_with_governor("https://api.alternative.me/fng/?limit=1")
            if fng_data and 'data' in fng_data:
                pulse['fear_and_greed'] = f"{int(fng_data['data'][0]['value'])} ({fng_data['data'][0]['value_classification']})"
        except Exception: pass
        try:
            global_data = self._fetch_with_governor(f"{self.coingecko_api_base}/global")
            if global_data and 'data' in global_data:
                btc_dominance = global_data['data'].get('market_cap_percentage', {}).get('btc')
                if btc_dominance: pulse['btc_dominance'] = f"{btc_dominance:.2f}"
        except Exception: pass
        return pulse

    def _is_db_empty(self, cursor):
        cursor.execute("SELECT COUNT(id) FROM coins")
        return cursor.fetchone()[0] < 100

    def _run_genesis_protocol(self, cursor):
        logger.info("जेनेसिस प्रोटोकल सक्रिय: पहिलो पटकको लागि पूर्ण ब्रह्माण्ड निर्माण गर्दै...")
        for page in range(1, 21):
            logger.info(f"जेनेसिस: पृष्ठ {page}/20 स्क्यान गर्दै...")
            params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 250, 'page': page}
            market_data = self._fetch_with_governor(f"{self.coingecko_api_base}/coins/markets", params=params)
            if not market_data: continue
            for coin in market_data:
                cursor.execute("INSERT INTO coins (symbol, name, coingecko_id) VALUES (?, ?, ?) ON CONFLICT(coingecko_id) DO NOTHING", (coin['symbol'].upper(), coin['name'], coin['id']))

    def update_universe_incrementally(self):
        conn = get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            if self._is_db_empty(cursor): self._run_genesis_protocol(cursor); conn.commit()
            stale_threshold = datetime.utcnow() - timedelta(hours=6)
            cursor.execute("SELECT coingecko_id FROM coins WHERE last_seen < ?", (stale_threshold,))
            ids_to_fetch = [row['coingecko_id'] for row in cursor.fetchall()]
            if not ids_to_fetch: logger.info("सबै सिक्काहरू ताजा छन्।"); return
            logger.info(f"कुल {len(ids_to_fetch)} पुराना सिक्काहरूको लागि बजार डाटा मागिँदैछ...")
            updated_coins = 0
            for i in range(0, len(ids_to_fetch), 250):
                batch_ids = ids_to_fetch[i:i+250]
                params = {'vs_currency': 'usd', 'ids': ",".join(batch_ids)}
                market_data = self._fetch_with_governor(f"{self.coingecko_api_base}/coins/markets", params=params)
                if not market_data: continue
                for coin in market_data:
                    cursor.execute("UPDATE coins SET price_usd=?, volume_24h=?, market_cap=?, last_seen=CURRENT_TIMESTAMP WHERE coingecko_id = ?", (coin.get('current_price',0), coin.get('total_volume',0), coin.get('market_cap',0), coin['id']))
                    updated_coins += 1
            conn.commit(); logger.info(f"✅ वृद्धिशील अपडेट सम्पन्न भयो। {updated_coins} सिक्काहरू सफलतापूर्वक अपडेट गरियो।")
        except Exception as e:
            logger.error(f"वृद्धिशील अपडेटमा त्रुटि: {e}", exc_info=True)
        finally:
            if conn: conn.close()

def run_data_collection_cycle():
    librarian = WiseLibrarian()
    market_pulse = librarian.get_market_pulse()
    librarian.update_universe_incrementally()
    return market_pulse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # --- समाधान: 'setup_database' को सट्टा 'ensure_database_integrity' लाई बोलाउने ---
    ensure_database_integrity()
    run_data_collection_cycle()
