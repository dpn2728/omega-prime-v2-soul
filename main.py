import os
import threading
import time
from flask import Flask
from market import get_market_data
from model import predict_with_quantum_brain
from alerts import send_decree_email

app = Flask(__name__)

# Global state to check if the first run is complete
FIRST_CYCLE_COMPLETE = False

@app.route('/')
def health_check():
    """
    Provides health status. Cloud Run uses this to know the app is alive.
    """
    if not FIRST_CYCLE_COMPLETE:
        return "Omega Prime AI Agent is alive. First cognitive cycle is running...", 202
    return "Omega Prime AI Agent is alive, watching, and thinking.", 200

def main_cognitive_loop():
    """
    The main AI logic loop. Runs in the background after a short delay.
    """
    global FIRST_CYCLE_COMPLETE
    print("Cognitive loop thread started. Waiting 15 seconds before first run...")
    time.sleep(15) # Give the Flask server time to start properly

    print("--- ओमेगा प्राइम संज्ञानात्मक लुप प्रारम्भ हुँदैछ ---")
    while True:
        print(f"\n--- नयाँ संज्ञानात्मक चक्र सुरु हुँदैछ [{time.strftime('%Y-%m-%d %H:%M:%S')}] ---")
        
        market_df = get_market_data()
        
        if market_df is not None and not market_df.empty:
            decision_data = predict_with_quantum_brain(market_df)
            send_decree_email(decision_data)
        else:
            print("बजार डाटा प्राप्त गर्न सकिएन। यो चक्रको लागि कुनै आदेश जारी गरिएन।")

        FIRST_CYCLE_COMPLETE = True
        print("--- संज्ञानात्मक चक्र पूरा भयो। २३ घण्टाको लागि विश्राम। ---")
        time.sleep(23 * 60 * 60)

if __name__ == "__main__":
    # Start the main AI logic in a background thread IMMEDIATELY
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()
    
    # Start the Flask web server IMMEDIATELY
    # This will respond to Cloud Run's health checks while the cognitive loop works.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
