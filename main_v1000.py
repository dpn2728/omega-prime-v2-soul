# main_v1000.py (v1.7 - The Final Calibration)

import logging, time
from datetime import datetime
import config
from database_manager import get_db_connection, ensure_database_integrity
from data_sources_v1000 import run_data_collection_cycle
from pre_cognitive_hunter import PreCognitiveHunter
import email_templates
from email_system import send_directive_email

logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', handlers=[ logging.FileHandler("omega_prime_history_v1000.log"), logging.StreamHandler() ])
logger = logging.getLogger("OmegaPrime.GodMachine")

def _calculate_scores(conn):
    cursor = conn.cursor()
    # --- समाधान: "अज्ञात सैनिक" हरूलाई पनि न्यायको लागि ल्याउने ---
    # हामी केवल coin_id भएका संकेतहरूलाई मात्र होइन, सबैलाई लिन्छौं।
    cursor.execute("""
        SELECT 
            c.id, c.symbol, c.name, c.price_usd, c.volume_24h, c.market_cap,
            s.weight
        FROM signals s
        LEFT JOIN coins c ON s.coin_id = c.id
    """)
    
    potential_candidates = {}
    for row in cursor.fetchall():
        # यदि सिक्का अज्ञात छ भने, हामी अस्थायी डाटा बनाउँछौं
        coin_id = row['id'] if row['id'] is not None else row['meta_json'] 
        if coin_id not in potential_candidates:
            potential_candidates[coin_id] = {
                "name": row['name'] or json.loads(row['meta_json']).get('token_symbol', 'Unknown'),
                "symbol": row['symbol'] or json.loads(row['meta_json']).get('token_symbol', 'N/A'),
                "price_usd": row['price_usd'] or 0,
                "volume_24h": row['volume_24h'] or 0,
                "market_cap": row['market_cap'] or 0,
                "signals": []
            }
        potential_candidates[coin_id]['signals'].append(row['weight'])

    scored_candidates = []
    for data in potential_candidates.values():
        market_momentum = min((data['volume_24h'] / data['market_cap']) * 100, 100) if data['market_cap'] > 0 else 0
        wallet_flow = sum(data['signals']) * 100
        
        # यदि सिक्का अज्ञात छ भने, उसको wallet_flow नै उसको मुख्य शक्ति हो
        if data['market_cap'] == 0:
            final_score = wallet_flow
        else:
            final_score = (0.30 * market_momentum) + (0.70 * wallet_flow)

        if final_score > 60:
            # Add logic to fetch more details for the email if needed
            scored_candidates.append({
                "name": data['name'], "symbol": data['symbol'], "final_score": final_score,
                # ... (rest of the email data dictionary)
            })
            
    return sorted(scored_candidates, key=lambda x: x['final_score'], reverse=True)


def run_god_machine_cycle():
    logger.info("="*60 + f"\n 👑 गड-मेसिन चक्र (v1.7 - अन्तिम क्यालिब्रेसन) सुरु हुँदैछ\n" + "="*60)
    
    if not ensure_database_integrity():
        logger.critical("जग निर्माण हुन सकेन! चक्र रद्द गरियो।"); return

    market_pulse_data = run_data_collection_cycle()
    PreCognitiveHunter().hunt_for_wallet_flows()
    
    conn = get_db_connection()
    if not conn: return
    try:
        all_candidates = _calculate_scores(conn)
    finally:
        conn.close()
    
    if not all_candidates:
        logger.info("🌙 कुनै योग्य उम्मेदवार फेला परेन। होल्ड आदेश जारी गरिँदैछ।")
        # ... (hold directive logic is correct)
    else:
        logger.info(f"🔥 विजय! {len(all_candidates)} उच्च-सम्भावनाको उम्मेदवार(हरू) फेला परे।")
        best_candidate = all_candidates[0]
        # This part needs more data to generate the full email, which is the next step.
        # For now, it will send what it can.
        subject, html_body = email_templates.generate_genesis_directive(best_candidate)
        send_directive_email(subject, html_body)
    
    logger.info("✅ गड-मेसिन चक्र सफलतापूर्वक सम्पन्न भयो।")


if __name__ == "__main__":
    run_god_machine_cycle()
    logger.info(f"अर्को चक्र {config.MAIN_LOOP_SLEEP_HOURS} घण्टामा सुरु हुनेछ।")
