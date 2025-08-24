import os
import time
import threading
from flask import Flask, jsonify

# हाम्रो साम्राज्यका अन्य मोड्युलहरूलाई सही तरिकाले आयात गर्नुहोस्
# हामी अब 'model' बाट कुनै विशेष फंक्सन होइन, सम्पूर्ण मोड्युल नै आयात गर्छौं।
import market
import model
# import alerts  # संचार प्रणालीलाई अहिलेको लागि निष्क्रिय राखौं

# Flask एप सिर्जना गर्नुहोस् - यो हाम्रो AI को "धड्कन" हो
app = Flask(__name__)

# --- केन्द्रीय स्नायु प्रणाली ---
def main_cognitive_loop():
    """
    यो ओमेगा प्राइमको मस्तिष्क हो। यसले निरन्तर सोच्छ र काम गर्छ।
    """
    print("🧠 Omega Prime's cognitive loop initiated. The hunt begins...")
    # परीक्षणको लागि, अहिले एक पटक मात्र चलाऔं।
    # while True:
    try:
        # चरण १: ज्ञानेन्द्रियहरू (Senses) - बजार हेर्ने
        print("👁️ SENSE: Scanning the market...")
        market_data = market.get_market_data()

        # चरण २: मस्तिष्क (Mind) - निर्णय लिने
        # हामी अब सही फंक्सन 'model.generate_directive' लाई बोलाउँछौं।
        print("💡 MIND: Analyzing data and forming a directive...")
        directive = model.generate_directive(market_data)

        # चरण ३: सञ्चार (Communication) - आदेश जारी गर्ने
        print(f"🗣️ COMMUNICATE: Directive formulated -> Type: {directive.get('type')}, Reason: {directive.get('reason')}")
        # alerts.send_decree(directive) # वास्तविक इमेल पठाउने कामलाई अहिलेको लागि रोक्ने

        print("✅ Cognitive cycle complete. The Emperor has been served.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR in cognitive loop: {e}")

    # अर्को चक्रको लागि २३ घण्टा सुत्ने
    print("😴 System entering deep sleep for 23 hours...")
    # time.sleep(23 * 60 * 60)

@app.route('/')
def health_check():
    """
    Cloud Run लाई "म जीवित छु" भन्नका लागि।
    """
    return jsonify(status="ALIVE", message="Omega Prime v2.0 is thinking..."), 200

if __name__ == "__main__":
    # मुख्य संज्ञानात्मक चक्रलाई पृष्ठभूमिमा चलाउनुहोस्
    cognitive_thread = threading.Thread(target=main_cognitive_loop)
    cognitive_thread.daemon = True
    cognitive_thread.start()

    # Flask वेब सर्भर सुरु गर्नुहोस्
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
