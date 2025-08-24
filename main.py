import os
import time
import threading
from flask import Flask, jsonify

# हाम्रो साम्राज्यका मोड्युलहरू आयात गर्नुहोस्
import market
import model
# import alerts # संचार प्रणाली अर्को चरणमा सक्रिय गरिनेछ

# Flask एप सिर्जना गर्नुहोस् - यो हाम्रो AI को "धड्कन" हो
app = Flask(__name__)

# --- केन्द्रीय स्नायु प्रणाली (The Central Nervous System) ---
def main_cognitive_loop():
    """
    यो ओमेगा प्राइमको निरन्तर चल्ने मस्तिष्क हो।
    यसले कहिल्यै सुत्दैन, केवल रणनीतिक विश्राम लिन्छ।
    """
    print("🧠 Omega Prime's cognitive loop initiated for ETERNAL VIGILANCE.")
    
    while True:
        try:
            # चरण १: ज्ञानेन्द्रियहरू (Senses) - बजार हेर्ने
            print("👁️ SENSE: Scanning the market...")
            market_data = market.get_market_data()

            # चरण २: मस्तिष्क (Mind) - निर्णय लिने
            print("💡 MIND: Analyzing data and forming a directive...")
            directive = model.generate_directive(market_data)

            # चरण ३: सञ्चार (Communication) - आदेश जारी गर्ने
            print(f"🗣️ COMMUNICATE: Directive formulated -> Type: {directive.get('type')}, Reason: {directive.get('reason')}")
            # alerts.send_decree(directive) # अर्को चरणमा सक्रिय गरिनेछ

        except Exception as e:
            # त्रुटि हुँदा पनि प्रणालीलाई निरन्तर चलाइराख्ने
            print(f"❌ CRITICAL ERROR in cognitive loop: {e}")
            print("   Continuing the eternal hunt despite the error.")

        # अर्को चक्रको लागि रणनीतिक विश्राम
        # उत्पादनको लागि, यसलाई 60 * 60 (१ घण्टा) मा राख्नुहोस्।
        # परीक्षणको लागि, यसलाई 10 * 60 (१० मिनेट) मा राखौं।
        sleep_duration_seconds = 10 * 60
        print(f"✅ Cycle complete. Entering strategic pause for {sleep_duration_seconds / 60} minutes...")
        time.sleep(sleep_duration_seconds)

@app.route('/')
def health_check():
    """
    Cloud Run लाई "म जीवित छु" भन्नका लागि।
    """
    return jsonify(status="ALIVE", message="Omega Prime is on a 24/7 hunt."), 200

if __name__ == "__main__":
    # मुख्य संज्ञानात्मक चक्रलाई पृष्ठभूमिमा चलाउनुहोस्
    cognitive_thread = threading.Thread(target=main_cognitive_loop)
    cognitive_thread.daemon = True
    cognitive_thread.start()

    # Flask वेब सर्भर सुरु गर्नुहोस्
    port = int(os.environ.get("PORT", 8080))
    # debug=False उत्पादनको लागि महत्त्वपूर्ण छ।
    app.run(debug=False, host='0.0.0.0', port=port)
