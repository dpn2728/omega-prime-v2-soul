# main.py (v5.0 - The Grand Conductor of the Living Empire)

import logging
import time
from datetime import datetime

# --- साम्राज्यका सबै अन्तिम अंगहरूलाई एकसाथ ल्याउने ---
try:
    import config
    from system_monitor import SystemMonitor
    from update_system import UpdateManager, restart_application
    from data_sources import run_oracle_engine
    from tri_mind import run_council_consensus
    import email_templates
    from email_system import send_directive_email
except ImportError as e:
    print(f"FATAL ERROR: साम्राज्यको एक महत्त्वपूर्ण अंग हराएको छ: {e}")
    exit()

# --- लगिङ कन्फिगरेसन: साम्राज्यको इतिहास लेख्ने ---
logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    handlers=[ logging.FileHandler("omega_prime_history.log"), logging.StreamHandler() ]
)
logger = logging.getLogger("OmegaPrime.Conductor")

def main():
    """
    Omega Prime को महान् सञ्चालक।
    यसले साम्राज्यका सबै कार्यहरूलाई एक सुसंगत सिम्फनीमा अर्केस्ट्रेट गर्दछ।
    """
    logger.info("👑 सम्राट, जीवित साम्राज्य (v5.0) को महान् सञ्चालक जीवित भएको छ।")
    monitor = SystemMonitor(); monitor.start()

    while True:
        try:
            logger.info("="*60 + f"\n नयाँ चक्र सुरु हुँदैछ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "="*60)

            # --- चरण १: अमर फिनिक्स इन्जिन (आत्म-अपडेट) ---
            logger.info("[चरण १/५] अमर फिनिक्स इन्जिन: प्रणाली अपडेटहरूको लागि जाँच गर्दै...")
            updater = UpdateManager()
            if updater.run_update_cycle():
                logger.info("अपडेट सफल भयो! प्रणालीको आत्मालाई पुनर्जीवित गर्न पुनः सुरु गर्दै...")
                restart_application()
            logger.info("प्रणाली नवीनतम संस्करणमा छ।")

            # --- चरण २: ओरेकल इन्जिन (ज्ञान संश्लेषण) ---
            logger.info("[चरण २/५] ओरेकल इन्जिन: ब्रह्माण्डको ज्ञान संश्लेषण गर्दै...")
            candidate_coins, market_pulse_data = run_oracle_engine()

            # --- चरण ३: सम्राटको परिषद् (निर्णय र वर्गीकरण) ---
            logger.info("[चरण ३/५] सम्राटको परिषद्: अवसरहरूको विश्लेषण र वर्गीकरण गर्दै...")
            approved_opportunities = run_council_consensus(candidate_coins)

            # --- चरण ४: शाही उद्घोषक (सही आदेश जारी गर्ने) ---
            logger.info("[चरण ४/५] शाही उद्घोषक: सम्राटलाई सही आदेश पठाउँदै...")
            if not approved_opportunities:
                logger.info("🌙 कुनै पनि अवसरले परिषद्को मापदण्ड पूरा गरेन। होल्ड आदेश जारी गरिँदैछ।")
                subject, html_body = email_templates.generate_hold_directive(market_pulse_data)
                send_directive_email(subject, html_body)
            else:
                logger.info(f"✅ परिषद्ले {len(approved_opportunities)} अवसर(हरू) स्वीकृत गर्यो। आदेशहरू पठाइँदैछ...")
                for opportunity in approved_opportunities:
                    classification = opportunity.get('classification', 'NONE')
                    subject, html_body = None, None
                    
                    if classification == 'GENESIS':
                        subject, html_body = email_templates.generate_genesis_directive(opportunity)
                    elif classification == 'SLEEPING_GIANT':
                        subject, html_body = email_templates.generate_sleeping_giant_directive(opportunity)
                    elif classification == 'BLACK_SWAN':
                        subject, html_body = email_templates.generate_black_swan_directive(opportunity)
                    elif classification == 'URGENT_ALPHA':
                        subject, html_body = email_templates.generate_urgent_alpha_alert(opportunity)
                    
                    if subject and html_body:
                        logger.info(f"'{opportunity['symbol']}' को लागि '{classification}' प्रकारको आदेश पठाइँदैछ।")
                        send_directive_email(subject, html_body)

            # --- चरण ५: निद्रा र पुनरावृत्ति ---
            sleep_duration_seconds = config.MAIN_LOOP_SLEEP_HOURS * 3600
            logger.info(f"[चरण ५/५] सिम्फनी सम्पन्न। अर्को चक्र {config.MAIN_LOOP_SLEEP_HOURS} घण्टामा सुरु हुनेछ।")
            monitor.update_heartbeat()
            time.sleep(sleep_duration_seconds)

        except KeyboardInterrupt:
            logger.info("सम्राटको आदेशमा प्रणाली बन्द गरिँदैछ।")
            break
        except Exception as e:
            logger.critical(f"FATAL CONDUCTOR ERROR: {e}", exc_info=True)
            time.sleep(300)

    monitor.stop()
    logger.info("👑 महान् सञ्चालक सफलतापूर्वक बन्द भयो।")

if __name__ == "__main__":
    main()
