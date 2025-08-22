import os
import threading
import time
from flask import Flask
from market import get_market_data
# from indicators import apply_technical_indicators # <-- Temporarily disable this sense

# --- Flask App Definition ---
app = Flask(__name__)

@app.route('/')
def health_check():
    # Update the health check message
    return "Omega Prime AI Agent is alive and seeing. Analysis module is on standby.", 200

def main_cognitive_loop():
    """
    The main AI logic loop. It runs continuously in the background.
    """
    print("--- Omega Prime Cognitive Loop Initializing ---")
    while True:
        print("\n--- Starting new cognitive cycle ---")

        # Step 1: Perceive the market
        market_df = get_market_data()

        if market_df is not None and not market_df.empty:
            # The analysis step is temporarily disabled until we add historical data.
            # analyzed_df = apply_technical_indicators(market_df)

            # For now, we will just print the data we have.
            print("Top 5 coins found under $2 (Analysis module on standby):")
            report_df = market_df[['name', 'current_price', 'market_cap']].head(5)
            print(report_df.to_string())
        else:
            print("Could not retrieve market data. Skipping this cycle.")

        print("--- Cognitive cycle complete. Sleeping for 1 hour. ---")
        time.sleep(3600)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
