import os
import threading
import time
from flask import Flask
from market import get_market_data
from model import predict_with_quantum_brain
from alerts import send_decree_email
import traceback

app = Flask(__name__)

FIRST_CYCLE_COMPLETE = False

@app.route('/')
def health_check():
    if not FIRST_CYCLE_COMPLETE:
        return "Omega Prime AI Agent is alive. First cognitive cycle is running...", 202
    return "Omega Prime AI Agent is alive, watching, and thinking.", 200

def main_cognitive_loop():
    """
    The main AI logic loop, now in Diagnostic Mode with verbose logging.
    """
    global FIRST_CYCLE_COMPLETE
    print("Cognitive loop thread started. Waiting 15 seconds before first run...")
    time.sleep(15)

    print("--- ओमेगा प्राइम संज्ञानात्मक लुप प्रारम्भ हुँदैछ ---")
    while True:
        try:
            print(f"\n--- नयाँ संज्ञानात्मक चक्र सुरु हुँदैछ [{time.strftime('%Y-%m-%d %H:%M:%S')}] ---")
            
            print("[MAIN - DIAGNOSTIC]: Calling market.py to get market data...")
            market_df = get_market_data()
            print("[MAIN - DIAGNOSTIC]: market.py finished.")
            
            if market_df is not None and not market_df.empty:
                print("[MAIN - DIAGNOSTIC]: Market data received. Calling model.py to get a decision...")
                decision_data = predict_with_quantum_brain(market_df)
                print(f"[MAIN - DIAGNOSTIC]: model.py finished. Directive is '{decision_data.get('directive_type')}'.")

                print("[MAIN - DIAGNOSTIC]: Calling alerts.py to send the decree...")
                send_decree_email(decision_data)
                print("[MAIN - DIAGNOSTIC]: alerts.py finished.")
            else:
                print("[MAIN - DIAGNOSTIC]: No market data received from market.py. Skipping cycle.")

            FIRST_CYCLE_COMPLETE = True
            print("--- संज्ञानात्मक चक्र पूरा भयो। २३ घण्टाको लागि विश्राम। ---")
            time.sleep(23 * 60 * 60)
        except Exception as e:
            # This is a master safety net to catch any unexpected error in the loop
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!! FATAL ERROR in main_cognitive_loop !!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            traceback.print_exc()
            print("--- Waiting for 5 minutes before retrying to avoid crash loops ---")
            time.sleep(300)

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_cognitive_loop, daemon=True)
    main_thread.start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
