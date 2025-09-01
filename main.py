# main.py (v5.0 - The Omega Prime "Emperor's Hand" - FINAL AUTONOMOUS CORE)

import logging
import time
import sys
import os
import json
from datetime import datetime, timedelta

# --- OMEGA PRIME'S LIVING ORGANS (सबै मोड्युलहरू आयात गर्ने) ---
try:
    from config import is_configured_correctly, get_logger_config, EXECUTION_CONFIG
    from system_monitor import SystemMonitor
    from update_system import UpdateManager, restart_application
    from data_sources import scan_universe_and_analyze
    from tri_mind import run_tri_mind_consensus_for_batch
    import email_templates
    from email_system import send_directive_email
    from execution_engine import ExecutionEngine # <-- सम्राटको हात (The Emperor's Hand)
except ImportError as e:
    print(f"FATAL ERROR: A core module is missing: {e}. Please ensure all .py files are present.")
    sys.exit(1)

# --- ग्लोबल कन्फिगरेसन ---
MAIN_LOOP_INTERVAL_SECONDS = 28800  # 8 hours
ERROR_RESTART_DELAY_SECONDS = 300   # 5 minutes
DIRECTIVE_LOG_FILE = "sent_directives.log"

# --- स्मार्ट मेमोरी हेल्पर कार्यहरू ( अपरिवर्तित ) ---
def has_been_sent_recently(symbol, log_file=DIRECTIVE_LOG_FILE, hours=24):
    if not os.path.exists(log_file): return False
    now = datetime.now()
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get('symbol') == symbol:
                        log_time = datetime.fromisoformat(data.get('timestamp'))
                        if (now - log_time) < timedelta(hours=hours):
                            return True
                except (json.JSONDecodeError, KeyError, TypeError): continue
    except Exception as e:
        logging.error(f"स्मार्ट मेमोरी लग फाइल पढ्दा त्रुटि: {e}")
    return False

def log_sent_directive(symbol, trade_info, log_file=DIRECTIVE_LOG_FILE):
    log_entry = {
        'symbol': symbol, 
        'timestamp': datetime.now().isoformat(),
        'trade_info': trade_info
    }
    try:
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        logging.error(f"स्मार्ट मेमोरी लग फाइलमा लेख्दा त्रुटि: {e}")

# --- प्रणाली सेटअप कार्यहरू ( अपरिवर्तित ) ---
def setup_advanced_logging():
    log_config = get_logger_config()
    logger = logging.getLogger()
    logger.setLevel(log_config['level'])
    if logger.hasHandlers(): logger.handlers.clear()
    formatter = logging.Formatter(log_config['format'])
    # ... (rest of the logging setup is unchanged) ...
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(log_config['log_file'])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    error_file_handler = logging.FileHandler(log_config['error_log_file'])
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)
    logging.info("="*60 + "\nउन्नत लगिङ प्रणाली सफलतापूर्वक कन्फिगर भयो।\n" + "="*60)

def check_for_updates():
    logging.info("अमर फिनिक्स इन्जिन सक्रिय: अपडेटहरूको लागि जाँच गर्दै...")
    updater = UpdateManager()
    if updater.run_update_cycle():
        logging.info("अपडेट सफल भयो। प्रणालीको नयाँ संस्करण सुरु गर्न पुनः सुरु हुँदैछ...")
        restart_application()
    else:
        logging.info("प्रणाली पहिले नै नवीनतम संस्करणमा छ।")

# --- v5.0 FINAL: The Main Autonomous Engine ---
def main():
    logging.info("👑 OMEGA PRIME ENGINE v5.0 - सम्राटको हात (स्वायत्त कोर) सुरु भयो 👑")
    system_monitor = SystemMonitor()
    system_monitor.start()

    # --- सम्राटको हातलाई सशस्त्र बनाउने ---
    execution_engine = ExecutionEngine(
        exchange_id=EXECUTION_CONFIG['default_exchange'],
        simulation_mode=EXECUTION_CONFIG['simulation_mode']
    )

    while True:
        try:
            check_for_updates()
            logging.info(f"--- नयाँ स्क्यान चक्र सुरु भयो: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            system_monitor.update_heartbeat()

            analyzed_coins = scan_universe_and_analyze()
            approved_candidates = run_tri_mind_consensus_for_batch(analyzed_coins if analyzed_coins else [])
            
            if approved_candidates:
                best_candidate_symbol = approved_candidates[0]['symbol']
                if has_been_sent_recently(best_candidate_symbol):
                    logging.info(f"स्मार्ट मेमोरी: {best_candidate_symbol} को लागि पहिले नै डाइरेक्टिभ पठाइएको छ।")
                else:
                    best_candidate_data = next((c for c in analyzed_coins if c['symbol'] == best_candidate_symbol), None)
                    if best_candidate_data:
                        logging.info(f"🔥🔥🔥 जेनेसिस उम्मेदवार फेला पर्यो: {best_candidate_data['name']} ({best_candidate_symbol}) 🔥🔥🔥")
                        
                        # <<< --- सम्राटको हात (THE EMPEROR'S HAND) IN ACTION --- >>>
                        logging.info(f"सम्राटको हात सक्रिय: {best_candidate_symbol} को लागि ट्रेड कार्यान्वयन गर्ने प्रयास गर्दै...")
                        trade_result = execution_engine.execute_buy_order(
                            symbol=best_candidate_symbol,
                            usdt_amount=EXECUTION_CONFIG['trade_amount_usdt']
                        )
                        # <<< --- ACTION COMPLETE --- >>>

                        if trade_result:
                            logging.info(f"ट्रेड कार्यान्वयन सफल (Order ID: {trade_result.get('id')})। जेनेसिस डाइरेक्टिभ पठाउँदै...")
                            subject, html_body = email_templates.generate_genesis_directive(best_candidate_data, {'prophet': True, 'strategist': True, 'guardian': True})
                            if send_directive_email(subject, html_body):
                                log_sent_directive(best_candidate_symbol, trade_result)
                        else:
                            logging.error(f"सम्राटको हात: {best_candidate_symbol} को लागि ट्रेड कार्यान्वयन गर्न असफल। डाइरेक्टिभ रद्द गरियो।")
            else:
                logging.info("🌙 कुनै उच्च-सम्भावनाको अवसर फेला परेन। होल्ड डाइरेक्टिभ पठाउँदै।")
                market_data = {'state': 'Low Opportunity', 'action': 'Preserve capital.'}
                next_scan_hours = MAIN_LOOP_INTERVAL_SECONDS // 3600
                subject, html_body = email_templates.generate_hold_directive(market_data, next_scan_hours)
                send_directive_email(subject, html_body)

            logging.info(f"--- स्क्यान चक्र सफलतापूर्वक पूरा भयो ---")
            logging.info(f"{MAIN_LOOP_INTERVAL_SECONDS // 3600} घण्टाको लागि निद्रामा जाँदै...")
            time.sleep(MAIN_LOOP_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            logging.info("सम्राटको आदेशमा प्रणाली बन्द गरिँदैछ।")
            system_monitor.stop()
            break
        except Exception as e:
            logging.critical(f"मुख्य लूपमा एक गम्भीर, अप्रत्याशित त्रुटि भयो: {e}", exc_info=True)
            logging.info(f"{ERROR_RESTART_DELAY_SECONDS} सेकेन्ड पछि पुनः सुरु गर्ने प्रयास गर्दै...")
            time.sleep(ERROR_RESTART_DELAY_SECONDS)

if __name__ == "__main__":
    setup_advanced_logging()
    if not is_configured_correctly():
        logging.critical("प्रणाली सुरु हुन सकेन। कृपया `config.py` र `omega_secrets.py` जाँच गर्नुहोस्।")
        sys.exit(1)
    main()
