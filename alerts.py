import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager

# --- CONFIGURATION ---
PROJECT_ID = "omegaprimeai"
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD_SECRET_ID = "omega-prime-email-password"

def get_email_password():
    """Fetches the email password from Google Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching email password from Secret Manager: {e}")
        return None

def send_email_alert(directive, reason, candidate):
    """Sends a formatted email decree to the Emperor."""
    print(f"Preparing to send email alert for directive: {directive}")
    password = get_email_password()
    if not password:
        print("Could not send email: Password not available.")
        return

    subject = f"🔥 Omega Prime Daily Summary | {directive} Directive"
    body = f"""
🔥 Omega Prime - दैनिक आदेश

Directive ID: H-20250822-001 (Placeholder)
Omega संस्करण: v1000.1 (The Thinking Machine)

कार्यकारी सारांश (नेपाली):
ओमेगा प्राइमले आजको लागि "{directive}" आदेश जारी गरेको छ।

तर्क (Reasoning):
{reason}

"""

    if candidate is not None:
        body += f"""
सर्वोच्च उम्मेदवार (Top Candidate):
- नाम: {candidate.get('name', 'N/A')}
- हालको मूल्य: ${candidate.get('current_price', 0):.4f}
- बजार पूँजीकरण: ${candidate.get('market_cap', 0):,}
"""

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email alert successfully sent to the Emperor.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
