import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager

# Gmail App Password Secret fetch
def get_secret(secret_id="omega-prime-email-password"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/omegaprimeai/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

smtp_user = "dpn2728@gmail.com"
smtp_pass = get_secret()

# Email content
msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = smtp_user   # Send to yourself for testing
msg['Subject'] = "SMTP Test"
msg.attach(MIMEText("Hello! This is a Gmail SMTP test using App Password.", 'plain'))

# Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, smtp_user, msg.as_string())

print("✅ Email sent successfully!")
