# history_builder.py (v1.4 - The Royal Army Mandate)

import logging
import time
import os
from datetime import datetime

from database_manager import get_db_connection, ensure_database_integrity
from data_sources_v1000 import WiseLibrarian

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', handlers=[ logging.FileHandler("history_builder.log"), logging.StreamHandler() ])
logger = logging.getLogger("ImperialHistorian")

class SpecialistHistorian:
    def __init__(self):
        self.librarian = WiseLibrarian()
        self.librarian.governor_sleep_time = 4

    def build_history(self):
        logger.info("👑 शाही सेनाको आदेश (v1.4) सक्रिय।")
        conn = get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS historical_data (id INTEGER PRIMARY KEY, coin_id INTEGER NOT NULL, date TEXT NOT NULL, price REAL NOT NULL, UNIQUE(coin_id, date), FOREIGN KEY (coin_id) REFERENCES coins (id));")
            
            # --- समाधान: शाही सेना - शीर्ष २००० सिक्काहरूलाई लक्ष्य बनाउने ---
            cursor.execute("SELECT id, coingecko_id, name FROM coins WHERE coingecko_id NOT LIKE 'unknown_%' AND market_cap > 0 ORDER BY market_cap DESC LIMIT 2000")
            target_coins = cursor.fetchall()

            if not target_coins:
                logger.warning("इतिहास निर्माण गर्नको लागि डाटाबेसमा कुनै सिक्का फेला परेन।"); return

            total_coins = len(target_coins)
            logger.info(f"कुल {total_coins} शीर्ष सिक्काहरूको लागि १ वर्षको ऐतिहासिक डाटा निर्माण सुरु हुँदैछ...")

            for index, coin in enumerate(target_coins):
                try:
                    coin_db_id = coin['id']; coingecko_id = coin['coingecko_id']; coin_name = coin['name']
                    
                    # यदि यो सिक्काको इतिहास पहिले नै पूर्ण छ भने, त्यसलाई छोड्ने
                    cursor.execute("SELECT COUNT(id) FROM historical_data WHERE coin_id = ?", (coin_db_id,))
                    if cursor.fetchone()[0] > 360:
                        logger.debug(f"'{coin_name}' को इतिहास पहिले नै पूर्ण छ, छोडिँदैछ।")
                        continue

                    logger.info(f"[{index + 1}/{total_coins}] सिक्का '{coin_name}' को लागि इतिहास निर्माण गर्दै...")
                    
                    params = {'vs_currency': 'usd', 'days': '365', 'interval': 'daily'}
                    history_data = self.librarian._fetch_with_governor(f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart", params=params)

                    if history_data and 'prices' in history_data:
                        for price_point in history_data['prices']:
                            date_str = datetime.fromtimestamp(price_point[0] / 1000).strftime('%Y-%m-%d')
                            cursor.execute("INSERT OR IGNORE INTO historical_data (coin_id, date, price) VALUES (?, ?, ?)", (coin_db_id, date_str, price_point[1]))
                    else:
                        logger.warning(f"'{coin_name}' ({coingecko_id}) को लागि कुनै ऐतिहासिक डाटा फेला परेन।")
                except Exception as e:
                    logger.error(f"'{coin.get('name', 'Unknown')}' को लागि डाटा ल्याउन असफल। त्रुटि: {e}."); continue
            
            conn.commit()
            logger.info("✅✅✅ शाही सेनाको अभियान सम्पन्न भयो!")
            logger.info("अब ५ मिनेटमा कम्प्युटर स्वचालित रूपमा बन्द हुनेछ।")
            os.system("sudo shutdown +5")
        except Exception as e:
            logger.critical(f"ऐतिहासिक डाटा निर्माणमा गम्भीर त्रुटि भयो: {e}", exc_info=True)
        finally:
            conn.close()

if __name__ == "__main__":
    ensure_database_integrity()
    historian = SpecialistHistorian()
    historian.build_history()
