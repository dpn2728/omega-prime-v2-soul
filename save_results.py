import json
import csv
from datetime import datetime

# उदाहरण: analysis_results list
analysis_results = [
    {"symbol": "GOOD", "final_verdict": "APPROVED", "confidence": 95},
    {"symbol": "RISK", "final_verdict": "REJECTED", "confidence": 40},
]

# --- JSON मा save गर्ने function ---
def save_json(results, filename=None):
    if not filename:
        filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    print(f"✅ JSON मा save भयो: {filename}")

# --- CSV मा save गर्ने function ---
def save_csv(results, filename=None):
    if not filename:
        filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    keys = results[0].keys() if results else []
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"✅ CSV मा save भयो: {filename}")

# --- auto-save चलाउने ---
save_json(analysis_results)
save_csv(analysis_results)
