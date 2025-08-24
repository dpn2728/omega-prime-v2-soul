import os # <-- The missing import has been added!
import threading
import time
from flask import Flask, jsonify
import market
import model
import alerts
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - PRIME MINISTER - %(levelname)s - %(message)s')

app = Flask(__name__)

def cognitive_loop():
    logging.info("🧠 Omega Prime's eternal hunt has begun...")
    while True:
        try:
            logging.info("\n--- New Hunt Cycle Initiated ---")
            market_data = market.get_market_data()
            directive = model.generate_directive(market_data)
            alerts.send_decree(directive)
        except Exception as e:
            logging.error(f"🔥🔥🔥 CRITICAL FAILURE in cognitive_loop: {e}")
        finally:
            pause_minutes = 10
            logging.info(f"--- Hunt Cycle Concluded. Pausing for {pause_minutes} minutes. ---")
            time.sleep(pause_minutes * 60)

@app.route('/')
def health_check():
    return "Omega Prime is ALIVE and hunting. Check logs for status.", 200

if __name__ == "__main__":
    hunt_thread = threading.Thread(target=cognitive_loop)
    hunt_thread.daemon = True
    hunt_thread.start()
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
