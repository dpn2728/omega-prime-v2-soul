import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager
import google.auth

def get_project_id():
    """
    स्वचालित रूपमा GCP प्रोजेक्ट ID पत्ता लगाउँछ। यो सबैभन्दा भरपर्दो तरिका हो।
    """
    try:
        _, project_id = google.auth.default()
        return project_id
    except google.auth.exceptions.DefaultCredentialsError:
        print("🔥 FATAL: Could not automatically determine GCP Project ID.")
        return None

# --- CONFIGURATION ---
PROJECT_ID = get_project_id()
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD_SECRET_ID = "omega-prime-email-password"

def get_email_password():
    """
    Secret Manager बाट इमेल पासवर्ड सुरक्षित रूपमा प्राप्त गर्छ।
    """
    if not PROJECT_ID:
        return None
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        response = client.access_secret_version(name=secret_name)
        password = response.payload.data.decode("UTF-8")
        return password
    except Exception as e:
        print(f"🔥 FATAL: Could not access the sacred password. Error: {e}")
        return None

# ... (बाँकी format_genesis_email, format_hold_email, send_decree फंक्सनहरू जस्ताको तस्तै रहनेछन्) ...

def format_genesis_email(directive):
    subject = f"🔥 Omega Prime Genesis Directive | {directive.get('coin_name', 'N/A')}"
    body = f"""
    🔥 Omega Prime - जेनेसिस आदेश 🔥
    =================================
    Directive Type: {directive.get('type')}
    Coin: {directive.get('coin_name', 'N/A')} ({directive.get('coin_symbol', 'N/A')})
    Current Price: ${directive.get('current_price', 0):.4f}
    24h Change: {directive.get('price_change_24h', 0):.2f}%

    Reasoning:
    {directive.get('reason', 'No specific reason provided.')}
    """
    return subject, body

def format_hold_email(directive):
    subject = "Holding Position | Omega Prime Market Intel"
    body = f"""
    🛡️ Omega Prime - होल्ड आदेश 🛡️
    =================================
    Directive Type: {directive.get('type')}
    
    Reasoning:
    {directive.get('reason', 'No specific reason provided.')}

    Capital is preserved. Patience is a virtue.
    """
    return subject, body

def send_decree(directive):
    print("SCRIBE: The Royal Scribe is preparing the decree...")
    password = get_email_password()
    if not password:
        print("SCRIBE: Cannot send email. The sacred password is unobtainable.")
        return

    directive_type = directive.get('type')
    if directive_type == "GENESIS":
        subject, body = format_genesis_email(directive)
    elif directive_type == "HOLD":
        subject, body = format_hold_email(directive)
    else:
        print(f"SCRIBE: Unknown directive type '{directive_type}'. Cannot format email.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ DECREE SENT: The '{directive_type}' decree has been successfully dispatched to the Emperor.")

    except smtplib.SMTPAuthenticationError as e:
        print(f"🔥 FATAL SMTP ERROR: Authentication failed. Error: {e}")
    except Exception as e:
        print(f"🔥 FATAL EMAIL ERROR: An unexpected error occurred. Error: {e}")
