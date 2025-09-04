# prophecy_engine.py (v1.0 - The Imperial Prophecy Engine)

import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

from database_manager import get_db_connection

logger = logging.getLogger(__name__)

class ProphecyEngine:
    """
    "The Four-Fold Prophecy" लाई शक्ति दिनको लागि, ऐतिहासिक डाटाको आधारमा
    मेसिन लर्निङको प्रयोग गरेर भविष्यको मूल्य भविष्यवाणीहरू उत्पन्न गर्दछ।
    """
    def __init__(self):
        self.conn = get_db_connection()

    def _get_historical_data_for_coin(self, coin_id, days=90):
        """डाटाबेसबाट एउटा सिक्काको लागि पछिल्लो 'days' को ऐतिहासिक डाटा ल्याउँछ।"""
        if not self.conn: return None
        try:
            cursor = self.conn.cursor()
            ninety_days_ago = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT date, price FROM historical_data
                WHERE coin_id = ? AND date >= ?
                ORDER BY date ASC
            """, (coin_id, ninety_days_ago))
            
            data = cursor.fetchall()
            return [row['price'] for row in data]
        except Exception as e:
            logger.error(f"सिक्का ID {coin_id} को लागि ऐतिहासिक डाटा ल्याउन असफल: {e}")
            return None

    def generate_prophecy(self, coin_id):
        """
        एउटा सिक्काको लागि "चार-पत्रे भविष्यवाणी" उत्पन्न गर्दछ।
        :return: A dictionary with predictions or None if not possible.
        """
        logger.debug(f"सिक्का ID {coin_id} को लागि भविष्यवाणी उत्पन्न गर्दै...")
        prices = self._get_historical_data_for_coin(coin_id, days=90)

        # भविष्यवाणी गर्नको लागि कम्तिमा ३० दिनको डाटा आवश्यक छ
        if not prices or len(prices) < 30:
            logger.warning(f"सिक्का ID {coin_id} को लागि भविष्यवाणी गर्न अपर्याप्त ऐतिहासिक डाटा ({len(prices) if prices else 0} दिन)।")
            return None

        try:
            # --- मेसिन लर्निङ मोडेलको तयारी ---
            # X = दिनहरू (0, 1, 2, ...), y = मूल्यहरू
            X = np.arange(len(prices)).reshape(-1, 1)
            y = np.array(prices)

            # --- प्रवृत्ति-आधारित मोडेललाई तालिम दिने ---
            model = LinearRegression()
            model.fit(X, y)

            # --- भविष्यको लागि भविष्यवाणी गर्ने ---
            future_days = np.array([
                len(prices) + 7,   # ७ दिन पछि
                len(prices) + 14,  # १४ दिन पछि
                len(prices) + 30   # ३० दिन पछि
            ]).reshape(-1, 1)

            predictions = model.predict(future_days)

            # भविष्यवाणीहरू नकारात्मक हुन सक्दैनन्
            predictions = [max(0, p) for p in predictions]

            prophecy = {
                "pred_7d": f"{predictions[0]:.4f}",
                "pred_14d": f"{predictions[1]:.4f}",
                "pred_30d": f"{predictions[2]:.4f}",
                "confidence": "Based on 90-day linear trend"
            }
            logger.info(f"सिक्का ID {coin_id} को लागि भविष्यवाणी सफल: {prophecy}")
            return prophecy

        except Exception as e:
            logger.error(f"सिक्का ID {coin_id} को लागि मेसिन लर्निङ भविष्यवाणीमा त्रुटि: {e}")
            return None

    def close(self):
        """डाटाबेस जडान बन्द गर्दछ।"""
        if self.conn:
            self.conn.close()

# --- यो फाइल सीधै चलाएर परीक्षण गर्न ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    engine = ProphecyEngine()
    if engine.conn:
        try:
            # उदाहरणको लागि: डाटाबेसमा भएको पहिलो सिक्काको भविष्यवाणी गर्ने
            cursor = engine.conn.cursor()
            cursor.execute("SELECT id, name FROM coins WHERE coingecko_id IS NOT NULL AND coingecko_id NOT LIKE 'unknown_%' LIMIT 1")
            first_coin = cursor.fetchone()
            
            if first_coin:
                logger.info(f"'{first_coin['name']}' (ID: {first_coin['id']}) को लागि भविष्यवाणीको परीक्षण गर्दै...")
                prophecy = engine.generate_prophecy(first_coin['id'])
                if prophecy:
                    print("\n--- भविष्यवाणी सफल ---")
                    print(f"   7-Day Target:  ~${prophecy['pred_7d']}")
                    print(f"  14-Day Target:  ~${prophecy['pred_14d']}")
                    print(f"  30-Day Target:  ~${prophecy['pred_30d']}")
                    print("----------------------")
                else:
                    print("भविष्यवाणी उत्पन्न गर्न सकिएन।")
            else:
                print("परीक्षण गर्नको लागि डाटाबेसमा कुनै योग्य सिक्का फेला परेन।")
        finally:
            engine.close()
    else:
        print("डाटाबेस जडान हुन सकेन।")
