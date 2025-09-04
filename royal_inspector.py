# royal_inspector.py (v1.5 - The Inspector Speaks)
import logging
import time

# --- साम्राज्यका सबै अंगहरूलाई निरीक्षणको लागि बोलाउने ---
import config
from database_manager import get_db_connection
from intelligence_aggregator import IntelligenceAggregator
from pre_cognitive_hunter import PreCognitiveHunter

# हामी यहाँ लगिङलाई शान्त राख्छौं ताकि हाम्रो रिपोर्ट सफा देखियोस्
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')

def run_inspection():
    """
    यो शाही निरीक्षक हो। यसले गड-मेसिनको मस्तिष्कको हरेक निर्णयको
    विस्तृत र अकाट्य रिपोर्ट प्रस्तुत गर्छ।
    """
    print("\n" + "="*80)
    print("👑 शाही निरीक्षण प्रोटोकल (v1.5) सक्रिय। सत्यको ऐना सक्रिय गरिँदैछ...")
    print("="*80 + "\n")

    conn = get_db_connection()
    if not conn:
        print("🔴 FATAL: साम्राज्यको मस्तिष्क (डाटाबेस) सँग जडान हुन सकेन।")
        return

    print("🔍 चरण १/३: पूर्व-संज्ञानात्मक शिकारीलाई तैनाथ गरिँदैछ (यो मौन रूपमा चल्छ)...")
    PreCognitiveHunter().hunt_for_wallet_flows()
    print("✅ शिकारीले आफ्नो रिपोर्ट पेश गर्यो।\n")

    try:
        aggregator = IntelligenceAggregator()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM coins 
            WHERE price_usd IS NOT NULL AND volume_24h IS NOT NULL AND market_cap IS NOT NULL
            AND price_usd < ? AND volume_24h > ? AND market_cap > 0 
            ORDER BY market_cap DESC LIMIT 50
        """, (
            config.MARKET_PARAMETERS['max_coin_price'], 
            config.MARKET_PARAMETERS['min_volume_24h']
        ))
        candidate_coins = [dict(row) for row in cursor.fetchall()]
        
        if not candidate_coins:
            print("🟡 चेतावनी: सुनौलो फिल्टर पास गर्ने कुनै योग्य उम्मेदवार भेटिएन।")
            return
            
        print(f"🔍 चरण २/३: शीर्ष {len(candidate_coins)} योग्य उम्मेदवारहरूको विश्लेषण सुरु हुँदैछ...")
        
        symbols = [c['symbol'] for c in candidate_coins]
        sentiments = aggregator.aggregate_intelligence_in_batch(symbols)
        
        print(f"\n{'Coin':<15} | {'Wallet Flow':<12} | {'Momentum':<10} | {'Narrative':<10} | {'FINAL SCORE':<12}")
        print("-"*80)

        for coin in candidate_coins:
            try:
                cursor.execute("SELECT weight FROM signals WHERE coin_id = ?", (coin['id'],))
                wallet_flow_raw = sum(s['weight'] for s in cursor.fetchall()) * 100
                sentiment_score = sentiments.get(coin['symbol'], 0.0)
                narrative_strength_raw = (sentiment_score + 1) * 50
                market_momentum_raw = min((coin['volume_24h'] / coin['market_cap']) * 100, 100)
                
                final_score = (
                    (0.20 * market_momentum_raw) + 
                    (0.50 * wallet_flow_raw) +
                    (0.30 * narrative_strength_raw)
                )
                print(f"{coin['symbol']:<15} | {wallet_flow_raw:<12.1f} | {market_momentum_raw:<10.1f} | {narrative_strength_raw:<10.1f} | {final_score:<12.2f} {'✅' if final_score > 65 else '❌'}")
            except Exception as e:
                print(f"{coin['symbol']:<15} | ERROR: {e}")

        print("\n" + "="*80)
        print("🔍 चरण ३/३: निरीक्षण सम्पन्न।")
        print("="*80)

    finally:
        conn.close()

# --- समाधान: निरीक्षकलाई स्टेजमा जान आदेश दिने ---
if __name__ == "__main__":
    run_inspection()
