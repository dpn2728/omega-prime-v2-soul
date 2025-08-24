import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = "ehtcrkyellbgwbvy"

def send_decree(directive):
    print(f"SCRIBE: Preparing to dispatch the '{directive['type']}' decree about the hunt...")
    
    # विषय र मुख्य भाग बनाउने
    if directive.get('type') == 'GENESIS':
        subject = f"🔥 Omega Prime Genesis Directive | {directive.get('coin_name', 'N/A')}"
        body = f"A Genesis candidate has been identified during the hunt.\n\nCoin: {directive.get('coin_name', 'N/A')}\n\nReason: {directive.get('reason', 'N/A')}"
    else: # HOLD
        subject = "🛡️ Omega Prime - Holding Position After Hunt"
        body = f"The hunter found no suitable prey. A Hold directive has been issued.\n\nReason: {directive.get('reason', 'N/A')}"

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ DECREE SENT: The Emperor has been notified of the hunt's result.")
        return True
    except Exception as e:
        print(f"🔥 SCRIBE ERROR: Failed to send the hunt report. Error: {e}")
        return False
