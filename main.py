import os
import threading
import time
from flask import Flask, jsonify
import market
import model
import alerts
# ... (the rest of the proven main.py code) ...
app = Flask(__name__)
@app.route('/')
def health_check(): return "Omega Prime is ALIVE...", 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
