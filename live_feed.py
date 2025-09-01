# live_feed.py (Nano Omega Auto-Update Engine v1.1 - Robust)
import requests
import time
import logging
from omega_secrets import FREE_APIS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - FEED - %(message)s')

def fetch_free_data():
    live_data_snapshot = {}
    for name, url in FREE_APIS.items():
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, timeout=10, headers=headers)
            resp.raise_for_status()
            live_data_snapshot[name] = resp.json()
            logging.info(f"Successfully fetched '{name}'.")
        except Exception as e:
            # --- Store the error in a structured way ---
            live_data_snapshot[name] = {"error": True, "message": str(e)}
            logging.error(f"Failed to fetch '{name}': {e}")
    return live_data_snapshot

def start_live_feed(refresh_interval_seconds=60):
    logging.info(f"--- Omega Prime Live Feed Activated ---")
    logging.info(f"Refreshing data every {refresh_interval_seconds} seconds.")
    while True:
        snapshot = fetch_free_data()
        
        print("\n--- LIVE DATA SNAPSHOT ---")

        # --- THIS IS THE FIX: Check for errors before processing data ---
        
        # Fear & Greed Index
        fg_data = snapshot.get('fear_greed_index', {})
        if not fg_data.get('error'):
            fg_value = fg_data.get('data', [{}])[0].get('value_classification', 'N/A')
            print(f"Fear & Greed Index: {fg_value}")
        else:
            print(f"Fear & Greed Index: FAILED to fetch")

        # Binance BTC Price
        binance_data = snapshot.get('binance_ticker', {})
        if not binance_data.get('error') and isinstance(binance_data, list):
            btc_price = next((item['price'] for item in binance_data if item['symbol'] == 'BTCUSDT'), 'Not Found')
            print(f"BTC Price (from Binance): {btc_price}")
        else:
            print(f"BTC Price (from Binance): FAILED to fetch")

        print("-" * 28)
        
        time.sleep(refresh_interval_seconds)

if __name__ == "__main__":
    start_live_feed()
