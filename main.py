import os
import threading
import time
from flask import Flask
from market import get_market_data # <-- IMPORT OUR NEW SENSE

# --- Flask App Definition ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Omega Prime AI Agent is alive and seeing the market.", 200

def main_cognitive_loop():
    """
    The main AI logic loop. It runs continuously in the background.
    """
    print("--- Omega Prime Cognitive Loop Initializing ---")
    while True:
        print("\n--- Starting new cognitive cycle ---")

        # Step 1: Use the Market Eye to perceive the market
        market_df = get_market_data()

        if market_df is not None:
            # For now, we just print the names of the top 5 coins found
            top_5_coins = market_df.head(5)['name'].tolist()
            print(f"Top 5 coins currently under $2: {top_5_coins}")
        else:
            print("Could not retrieve market data. Skipping this cycle.")

        # Wait for 1 hour before the next cycle, as per the constitution
        print("--- Cognitive cycle complete. Sleeping for 1 hour. ---")
        time.sleep(3600)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
