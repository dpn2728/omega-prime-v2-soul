# test_alert.py (Final - Corrected Syntax)
import logging
from alerts import send_genesis_directive

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dummy_coin_details = {
    'name': 'NovaNet', 'symbol': 'NVN', 'id': 'novanet',
    'price_usd': 0.045, 'market_cap_usd': 45_000_000,
    'total_volume_usd': 20_000_000, 'percent_change_24h': 25.5,
    'holder_count': 12500, 'news_volume': 85,
}
dummy_conviction_score = 97.2

print("--- SIMULATING GENESIS DIRECTIVE ---")
send_genesis_directive(dummy_coin_details, dummy_conviction_score)
print("--- SIMULATION COMPLETE ---")
