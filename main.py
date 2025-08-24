from flask import Flask, jsonify
import alerts

app = Flask(__name__)

@app.route('/')
def health_check():
    return "The Genesis Block is ALIVE. Awaiting the final command.", 200

@app.route('/test-email')
def trigger_email():
    print("PRIME MINISTER: The Emperor has given the final command. Instructing the Scribe.")
    success = alerts.send_test_decree()
    if success:
        return "✅ DECREE SENT! Check the Royal Inbox and the logs!", 200
    else:
        return "🔥 DEFEAT! Check the logs for the reason.", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
