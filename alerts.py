import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SCRIBE - %(levelname)s - %(message)s')

EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = "ehtcrkyellbgwbvy" 

def send_decree(directive):
    logging.info("Preparing decree...")
    directive_type = directive.get('type', 'UNKNOWN')

    if directive_type == 'GENESIS':
        subject = f"🔥 Omega Prime Genesis Directive | {directive.get('coin_name', 'N/A')}"
        body = f"A Genesis candidate has been identified.\n\nCoin: {directive.get('coin_name', 'N/A')}\n\nReason: {directive.get('reason', 'N/A')}"
    elif directive_type == 'HOLD':
        subject = "🛡️ Omega Prime - Holding Position"
        body = f"A Hold directive has been issued.\n\nReason: {directive.get('reason', 'N/A')}"
    else:
        logging.warning(f"Unknown directive type '{directive_type}'. Halting.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        logging.info("Connecting to smtp.gmail.com:465...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        logging.info("Connection successful. Logging in...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        logging.info("Login successful. Sending email...")
        server.send_message(msg)
        server.quit()
        logging.info(f"✅ DECREE SENT: The '{directive_type}' decree has been dispatched.")

    except Exception as e:
        logging.error(f"🔥🔥🔥 THE SCRIBE HAS FALLEN. THE FINAL ENEMY IS: {e}")
        logging.error(f"FULL TRACEBACK: {traceback.format_exc()}")
