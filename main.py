from flask import Flask, jsonify
import threading
import time
import market
import model
import alerts

app = Flask(__name__)

def cognitive_loop():
    print("🧠 Omega Prime's eternal hunt has begun...")
    while True:
        print("\n--- New Hunt Cycle Initiated ---")
        # १. शिकार गर्ने (Hunt)
        market_data = market.get_market_data()
        # २. सोच्ने (Think)
        directive = model.generate_directive(market_data)
        # ३. रिपोर्ट गर्ने (Report)
        alerts.send_decree(directive)
        
        # १० मिनेटको रणनीतिक विश्राम
        pause_minutes = 10
        print(f"--- Hunt Cycle Complete. Pausing for {pause_minutes} minutes. ---")
        time.sleep(pause_minutes * 60)

@app.route('/')
def health_check():
    return "Omega Prime is ALIVE and conducting its eternal hunt.", 200

if __name__ == "__main__":
    # शिकार चक्रलाई पृष्ठभूमिमा चलाउने
    hunt_thread = threading.Thread(target=cognitive_loop)
    hunt_thread.daemon = True
    hunt_thread.start()
    
    # स्वास्थ्य जाँचको लागि वेब सर्भर चलाउने
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
