import os
import threading
import time
from flask import Flask
from market import get_market_data
from indicators import apply_technical_indicators # <-- IMPORT OUR NEW ABILITY

# --- Flask App Definition ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Omega Prime AI Agent is alive, seeing, and analyzing.", 200

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
            # Step 2: Analyze the perceived data
            # We need 'close' prices for indicators. CoinGecko provides 'current_price'.
            # Let's rename it for compatibility with pandas-ta.
            market_df.rename(columns={'current_price': 'close'}, inplace=True)
            analyzed_df = apply_technical_indicators(market_df)

            if analyzed_df is not None:
                # For now, let's print the analysis of the top 5 coins
                print("Analysis of top 5 coins under $2:")
                # Select only the columns we are interested in for the report
                report_df = analyzed_df[['name', 'close', 'RSI', 'SMA50']].head(5)
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
