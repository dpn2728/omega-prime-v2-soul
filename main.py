import os
import threading
import time
from flask import Flask
from market import get_market_data
from model import predict_with_quantum_brain # <-- IMPORT THE BRAIN

# --- Flask App Definition ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Omega Prime AI Agent is alive, seeing, and thinking.", 200

def main_cognitive_loop():
    """
    The main AI logic loop, now with a thinking brain.
    """
    print("--- Omega Prime Cognitive Loop Initializing ---")
    while True:
        print("\n--- Starting new cognitive cycle ---")

        # Step 1: Perceive the market
        market_df = get_market_data()

        if market_df is not None and not market_df.empty:
            # Step 2: Let the Quantum Brain think and make a decision
            directive, candidate, reason = predict_with_quantum_brain(market_df)

            print(f"=== OMEGA PRIME DAILY DIRECTIVE ===")
            print(f"Directive: {directive}")
            print(f"Reason: {reason}")
            if candidate is not None:
                print(f"Top Candidate: {candidate['name']} (${candidate['current_price']})")
            print(f"===================================")

        else:
            print("Could not retrieve market data. Skipping this cycle.")

        print("--- Cognitive cycle complete. Sleeping for 1 hour. ---")
        time.sleep(3600)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
