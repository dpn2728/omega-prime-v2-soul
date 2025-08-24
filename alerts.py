import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- प्रत्यक्ष शाही कन्फिगरेसन (नयाँ साँचो सहित) ---
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"

# सम्राटद्वारा प्रदान गरिएको नयाँ, शक्तिशाली शाही साँचो
EMAIL_PASSWORD = "ehtcrkyellbgwbvy" 

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
    print("SCRIBE: The Royal Scribe is preparing the decree with the NEW key.")
    
    directive_type = directive.get('type')
    if directive_type == "GENESIS":
        subject, body = format_genesis_email(directive)
    elif directive_type == "HOLD":
        subject, body = format_hold_email(directive)
    else:
        print(f"SCRIBE: Unknown directive type '{directive_type}'. Halting.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print("Connecting to smtp.gmail.com:465...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print("Connection successful. Logging in with new key...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        print("Login successful. Sending email...")
        server.send_message(msg)
        server.quit()
        print(f"✅ DECREE SENT: The '{directive_type}' decree has been successfully dispatched.")

    except smtplib.SMTPAuthenticationError as e:
        print(f"🔥 FATAL SMTP ERROR: Authentication failed. The NEW password 'ehtc...wbvy' is INCORRECT. Please generate a new App Password. Error: {e}")
    except Exception as e:
        print(f"🔥 FATAL EMAIL ERROR: An unexpected error occurred. Error: {e}")
