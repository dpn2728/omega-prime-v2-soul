# alerts.py (Royal Messenger v1.3 - Final Secrets Fix)
import logging
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# --- THIS IS THE CRITICAL FIX ---
from omega_secrets import SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL

def _send_email_alert(subject: str, body_html: str):
    logger = logging.getLogger("Alerts")
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        logger.error("Email credentials not in omega_secrets.py. Cannot send alert.")
        return
    msg = EmailMessage(); msg['Subject'] = subject
    msg['From'] = f"Omega Prime <{SENDER_EMAIL}>"; msg['To'] = RECIPIENT_EMAIL
    msg.set_content("Please enable HTML to view this message.")
    msg.add_alternative(body_html, subtype='html')
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls(context=context); smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Successfully sent email: '{subject}'")
    except Exception as e:
        logger.critical(f"CRITICAL: Failed to send email alert. Reason: {e}")

def send_genesis_directive(coin_details: dict, conviction_score: float):
    name = coin_details.get('name', 'N/A'); symbol = coin_details.get('symbol', 'N/A').upper()
    price_usd = coin_details.get('price_usd', 0.0) or 0.0
    change_24h = coin_details.get('percent_change_24h', 0.0) or 0.0
    subject = f"🔥 Omega Prime Genesis Directive | {name} ({symbol}) | Score: {conviction_score:.2f}%"
    body_html = f"<html><body><h2>Genesis Directive for {name}</h2><p>Conviction Score: {conviction_score:.2f}%</p><p>Price: ${price_usd:,.4f}</p><p>24h Change: +{change_24h:.2f}%</p></body></html>"
    _send_email_alert(subject, body_html)

def send_summary_report(stats: dict):
    subject = f"📊 Omega Prime | Daily Scan Summary | {stats.get('alerts_triggered_genesis', 0)} Genesis, {stats.get('alerts_triggered_crisis', 0)} Crisis"
    start_time_str = datetime.fromtimestamp(stats['start_time']).strftime('%Y-%m-%d %H:%M:%S UTC')
    body_html = f"""
    <html><body>
        <h2>📊 Omega Prime - Daily Scan Summary</h2>
        <p><strong>Total Duration:</strong> {stats.get('duration', 0):.2f} seconds</p>
        <p><strong>Assets with Positive Momentum:</strong> {stats.get('coins_filtered_positive', 0)}</p>
        <p><strong>Assets with Negative Momentum:</strong> {stats.get('coins_filtered_negative', 0)}</p>
        <hr>
        <p><strong>Genesis Directives Triggered:</strong> {stats.get('alerts_triggered_genesis', 0)}</p>
        <p><strong>Crisis Alerts Triggered:</strong> {stats.get('alerts_triggered_crisis', 0)}</p>
    </body></html>
    """
    _send_email_alert(subject, body_html)

def send_crisis_alert(coin_details: dict):
    name = coin_details.get('name', 'N/A'); symbol = coin_details.get('symbol', 'N/A').upper()
    change_24h = coin_details.get('percent_change_24h', 0.0) or 0.0
    price_usd = coin_details.get('price_usd', 0.0) or 0.0
    subject = f"🚨 Omega Prime CRYSIS ALERT: {name} ({symbol}) has dropped {change_24h:.2f}%!"
    body_html = f"""
    <html><head><style>.container{{border: 2px solid #E74C3C;}} h2{{color: #E74C3C;}}</style></head>
    <body><div class="container">
        <h2>🚨 Omega Prime - CRYSIS ALERT</h2>
        <p><strong>Asset:</strong> {name} ({symbol})</p>
        <p><strong>Current Price:</strong> ${price_usd:,.4f}</p>
        <p><strong>24h Change:</strong> <strong style="color: #E74C3C;">{change_24h:.2f}%</strong></p>
    </div></body></html>
    """
    _send_email_alert(subject, body_html)
