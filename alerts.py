import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# ... (the rest of the proven alerts.py code) ...
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = os.environ.get('OMEGA_PRIME_EMAIL_PASSWORD')
def send_decree(directive):
    if not EMAIL_PASSWORD: return
    # ... (full send_decree function) ...
