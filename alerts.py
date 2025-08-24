import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager
import google.auth

def get_project_id():
    print("[DEBUG] Attempting to get project ID...")
    try:
        _, project_id = google.auth.default()
        print(f"[DEBUG] Successfully found Project ID: {project_id}")
        return project_id
    except google.auth.exceptions.DefaultCredentialsError as e:
        print(f"🔥 FATAL: Could not automatically determine GCP Project ID. Error: {e}")
        return None

PROJECT_ID = get_project_id()
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD_SECRET_ID = "omega-prime-email-password"

def get_email_password():
    print("[DEBUG] Attempting to get email password from Secret Manager...")
    if not PROJECT_ID:
        print("[DEBUG] Cannot get password, PROJECT_ID is missing.")
        return None
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        print(f"[DEBUG] Accessing secret: {secret_name}")
        response = client.access_secret_version(name=secret_name)
        password = response.payload.data.decode("UTF-8")
        print("[DEBUG] Successfully retrieved password.")
        # सुरक्षाको लागि, पासवर्डको केही अंश मात्र लग गर्ने
        print(f"[DEBUG] Password starts with: {password[:2]}... ends with: {password[-2:]}")
        return password
    except Exception as e:
        print(f"🔥 FATAL: Could not access the sacred password. Error: {e}")
        return None

def format_genesis_email(directive):
    # ... (यो फंक्सन जस्ताको तस्तै रहनेछ) ...
    subject = f"🔥 Omega Prime Genesis Directive | {directive.get('coin_name', 'N/A')}"
    body = "..." # (For brevity)
    return subject, body

def format_hold_email(directive):
    # ... (यो फंक्सन जस्ताको तस्तै रहनेछ) ...
    subject = "Holding Position | Omega Prime Market Intel"
    body = "..." # (For brevity)
    return subject, body

def send_decree(directive):
    print("[DEBUG] send_decree function initiated.")
    password = get_email_password()
    if not password:
        print("SCRIBE: Halting process. Password not available.")
        return

    directive_type = directive.get('type')
    if directive_type not in ["GENESIS", "HOLD"]:
        print(f"SCRIBE: Unknown directive type '{directive_type}'. Halting.")
        return

    print(f"[DEBUG] Formatting email for directive type: {directive_type}")
    subject, body = (format_genesis_email(directive) if directive_type == "GENESIS" else format_hold_email(directive))

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print("[DEBUG] Connecting to SMTP server: smtp.gmail.com:465")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print("[DEBUG] SMTP server connection successful.")
        
        print("[DEBUG] Logging into SMTP server...")
        server.login(EMAIL_SENDER, password)
        print("[DEBUG] SMTP login successful.")

        print("[DEBUG] Sending the email...")
        server.send_message(msg)
        print("[DEBUG] Email sent command issued.")

        server.quit()
        print(f"✅ DECREE SENT: The '{directive_type}' decree has been successfully dispatched.")

    except smtplib.SMTPAuthenticationError as e:
        print(f"🔥 FATAL SMTP ERROR: Authentication failed. CHECK YOUR APP PASSWORD. Error: {e}")
    except Exception as e:
        print(f"🔥 FATAL EMAIL ERROR: An unexpected error occurred. Error: {e}")

# (format_genesis_email र format_hold_email को पूरा शरीर यहाँ समावेश हुनेछ)
# ...
