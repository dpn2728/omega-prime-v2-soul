import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- प्रत्यक्ष शाही कन्फिगरेसन (परीक्षणको लागि) ---
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD = "ehtcrkyellbgwbvy" 

print("--- शाही लेखकको प्रत्यक्ष परीक्षा सुरु ---")

try:
    # इमेलको विषय र मुख्य भाग बनाउने
    subject = "Omega Prime - Royal Scribe Test"
    body = "सम्राट, यो ओमेगा प्राइमको शाही लेखकको तर्फबाट एक परीक्षण सन्देश हो। यदि तपाईंले यो प्राप्त गर्नुभयो भने, मेरो साँचो र ठेगाना सही छ।"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Gmail को SMTP सर्भरसँग जडान गर्ने
    print(f"Connecting to smtp.gmail.com:465 as {EMAIL_SENDER}...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print("Connection successful.")

    # लगइन गर्ने
    print(f"Logging in with the key 'ehtc...wbvy'...")
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print("Login successful.")

    # इमेल पठाउने
    print(f"Sending test email to {EMAIL_RECEIVER}...")
    server.send_message(msg)
    print("Email sent command issued.")
    
    # जडान बन्द गर्ने
    server.quit()
    print("Connection closed.")
    print("\n✅✅✅ Test Email Sent Successfully! Please check your inbox. ✅✅✅")

except smtplib.SMTPAuthenticationError as e:
    print("\n🔥🔥🔥 FATAL SMTP ERROR: Authentication Failed. 🔥🔥🔥")
    print("The App Password 'ehtcrkyellbgwbvy' is INCORRECT or your Gmail account has security blocks.")
    print(f"Detailed Error: {e}")
except Exception as e:
    print(f"\n🔥🔥🔥 An unexpected error occurred: {e}")

print("--- शाही लेखकको प्रत्यक्ष परीक्षा समाप्त ---")
