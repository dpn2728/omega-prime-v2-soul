import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = os.environ.get('OMEGA_PRIME_EMAIL_PASSWORD')

def send_test_decree():
    try:
        if not EMAIL_PASSWORD:
            print("SCRIBE ERROR: The secret key (OMEGA_PRIME_EMAIL_PASSWORD) was not found!")
            return False
        
        subject = "Omega Prime - VICTORY AT LAST"
        body = "सम्राट, यदि तपाईंले यो प्राप्त गर्नुभयो भने, हाम्रो 'प्रोटोकल शून्य' सफल भयो। साम्राज्य पुनर्स्थापित भयो।"
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ VICTORY: The test decree has been dispatched!")
        return True
    except Exception as e:
        print(f"🔥 DEFEAT: The Scribe has fallen. The final enemy is: {e}")
        return False
