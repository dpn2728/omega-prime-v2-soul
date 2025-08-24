import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager

# --- CONFIGURATION ---
# हामी अब हार्डकोड गर्नुको सट्टा, वातावरण चर (environment variables) बाट कन्फिगरेसन लिनेछौं।
# यो एक व्यावसायिक र सुरक्षित अभ्यास हो।
PROJECT_ID = os.environ.get('GCP_PROJECT') # Cloud Run ले यो स्वचालित रूपमा प्रदान गर्छ
EMAIL_SENDER = "dpn2728@gmail.com" # तपाईंको प्रेषक इमेल
EMAIL_RECEIVER = "dpn2728@gmail.com" # तपाईंको प्रापक इमेल
EMAIL_PASSWORD_SECRET_ID = "omega-prime-email-password" # Secret Manager मा भएको Secret को ID

def get_email_password():
    """
    Secret Manager बाट इमेल पासवर्ड सुरक्षित रूपमा प्राप्त गर्छ।
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        response = client.access_secret_version(name=secret_name)
        password = response.payload.data.decode("UTF-8")
        return password
    except Exception as e:
        print(f"🔥 FATAL: Could not access the sacred password from Secret Manager: {e}")
        return None

def format_genesis_email(directive):
    """
    'Genesis' आदेशको लागि इमेलको विषय र मुख्य भाग बनाउँछ।
    """
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
    """
    'Hold' आदेशको लागि इमेलको विषय र मुख्य भाग बनाउँछ।
    """
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
    """
    मुख्य फंक्सन: प्राप्त आदेशको आधारमा सही इमेल पठाउँछ।
    """
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

        # Gmail को SMTP सर्भरसँग सुरक्षित जडान
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ DECREE SENT: The '{directive_type}' decree has been successfully dispatched to the Emperor.")

    except smtplib.SMTPAuthenticationError as e:
        print(f"🔥 FATAL SMTP ERROR: Authentication failed. Check your App Password. Error: {e}")
    except Exception as e:
        print(f"🔥 FATAL EMAIL ERROR: An unexpected error occurred. Error: {e}")
