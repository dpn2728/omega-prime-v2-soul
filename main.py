import os
import threading
import time
from flask import Flask
from market import get_market_data
from model import predict_with_quantum_brain
from alerts import send_decree_email # <-- IMPORT THE NEW ROYAL SCRIBE

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Omega Prime AI Agent is alive, thinking, and issuing decrees.", 200

def main_cognitive_loop():
    print("--- Omega Prime Cognitive Loop Initializing ---")
    while True:
        print("\n--- Starting new cognitive cycle ---")
        market_df = get_market_data()
        if market_df is not None and not market_df.empty:
            # Let the brain decide which decree to issue
            decision_data = predict_with_quantum_brain(market_df)
            
            # Send the specific decree to the Emperor
            send_decree_email(decision_data)
        else:
            print("Could not retrieve market data. No directive issued.")
        
        print("--- Cognitive cycle complete. Sleeping for 23 hours. ---")
        time.sleep(23 * 60 * 60)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
