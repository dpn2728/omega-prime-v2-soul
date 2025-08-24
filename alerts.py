import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = "ehtcrkyellbgwbvy"

def send_test_decree():
    try:
        subject = "Omega Prime - VICTORY IS AT HAND"
        body = "सम्राट, यदि तपाईंले यो प्राप्त गर्नुभयो भने, हाम्रो जेनेसिस ब्लक सफल भयो। शाही लेखक जीवित छ।"
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print("SCRIBE: Connecting to Gmail...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print("SCRIBE: Logging in with the proven key...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        print("SCRIBE: LOGIN SUCCESSFUL. Sending the final proof...")
        server.send_message(msg)
        server.quit()
        print("✅ VICTORY: The test decree has been dispatched!")
        return True
    except Exception as e:
        print(f"🔥 DEFEAT: The Scribe has fallen. The final enemy is: {e}")
        return False
