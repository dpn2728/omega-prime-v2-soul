import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import secretmanager
from datetime import datetime
import random

# --- CONFIGURATION ---
PROJECT_ID = "omegaprimeai"
EMAIL_SENDER = "dpn2728@gmail.com"
EMAIL_RECEIVER = "dpn2728@gmail.com"
EMAIL_PASSWORD_SECRET_ID = "omega-prime-email-password"

def get_email_password():
    # (This function remains the same)
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching email password: {e}")
        return None

def _build_genesis_html(decision_data):
    coin = decision_data['coin_data']
    strategy = decision_data['strategy']
    catalyst = decision_data['catalyst']
    links = decision_data['mission_links']
    
    # Using f-string for HTML template with inline CSS for compatibility
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background-color: #f4f4f4; color: #333; }}
            .container {{ max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            .header {{ background-color: #d32f2f; color: white; padding: 10px; text-align: center; border-radius: 8px 8px 0 0; }}
            h2, h3 {{ color: #d32f2f; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .summary {{ background-color: #fff3e0; padding: 15px; border-left: 5px solid #ff9800; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 Omega Prime - जेनेसिस आदेश</h1>
            </div>
            <p><b>Directive ID:</b> G-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}</p>
            <p><b>Timestamp:</b> {datetime.now().strftime('%B %d, %Y, %I:%M:%S %p')} (AEST)</p>
            <p><b>Omega संस्करण:</b> v2000.0 (The Strategist) | <b>Conviction Score: {decision_data['conviction_score']}%</b></p>
            
            <h3>कार्यकारी सारांश (नेपाली):</h3>
            <div class="summary">
                <p>ओमेगा प्राइमको क्वान्टम ब्रेनले, <b>{coin.get('name', 'N/A')} ({coin.get('symbol', 'N/A').upper()})</b> लाई आजको सर्वोच्च-विश्वास "Genesis" अवसरको रूपमा चिन्हित गरेको छ। {decision_data['summary']}</p>
            </div>

            <h3>💡 उत्प्रेरक र भविष्यको सम्भावना</h3>
            <table>
                <tr><th>विश्लेषण</th><th>निष्कर्ष</th></tr>
                <tr><td><b>कोर प्रविधि</b></td><td>{catalyst['कोर प्रविधि']}</td></tr>
                <tr><td><b>साझेदारी</b></td><td>{catalyst['साझेदारी']}</td></tr>
                <tr><td><b>भविष्यको मूल्य अनुमान</b></td><td>{catalyst['भविष्यको मूल्य अनुमान']}</td></tr>
            </table>

            <h3>📝 रणनीतिक कार्यान्वयन योजना</h3>
            <table>
                <tr><th>विश्लेषण</th><th>आदेश (Directive)</th></tr>
                <tr><td><b>Entry Zone</b></td><td>{strategy['Entry Zone']}</td></tr>
                <tr><td><b>Stop-loss</b></td><td>{strategy['Stop-loss']}</td></tr>
                <tr><td><b>Target (1yr)</b></td><td>{strategy['Target (1yr)']}</td></tr>
                <tr><td><b>Suggested Allocation</b></td><td>{strategy['Suggested Allocation']}</td></tr>
            </table>

            <h3>🛒 तिम्रो मिशन (Your Mission)</h3>
            <table>
                <tr><th>Exchange</th><th>Trading Pair</th><th>Direct Execution Link</th></tr>
                <tr><td><b>Gate.io</b></td><td>{coin.get('symbol', 'N/A').upper()}/USDT</td><td><a href="#">{links['Gate.io']}</a></td></tr>
                <tr><td><b>MEXC</b></td><td>{coin.get('symbol', 'N/A').upper()}/USDT</td><td><a href="#">{links['MEXC']}</a></td></tr>
                <tr><td><b>Uniswap (DEX)</b></td><td>WETH/{coin.get('symbol', 'N/A').upper()}</td><td><a href="#">{links['Uniswap (DEX)']}</a></td></tr>
                <tr><td><b>Website</b></td><td>Official Project</td><td><a href="#">{links['Website']}</a></td></tr>
                <tr><td><b>Whitepaper</b></td><td>Technical Details</td><td><a href="#">{links['Whitepaper']}</a></td></tr>
            </table>
        </div>
    </body>
    </html>
    """
    return "🔥 Omega Genesis Directive | Deep Research: " + coin.get('name', 'N/A'), html

def _build_hold_html(decision_data):
    coin = decision_data['coin_data']
    subject = "🔥 Omega Daily Summary | Hold Directive & Market Intel"
    html = f"""
    <html><body>
        <h2>🔥 Omega Prime - होल्ड आदेश</h2>
        <p><b>Timestamp:</b> {datetime.now().strftime('%B %d, %Y, %I:%M:%S %p')} (AEST)</p>
        <p><b>Omega संस्करण:</b> v2000.0 (The Strategist)</p>
        <hr>
        <h3>मुख्य सन्देश:</h3>
        <p>{decision_data['reason']}</p>
        <h3>उत्कृष्ट, तर अपर्याप्त उम्मेदवार:</h3>
        <p><b>नाम:</b> {coin.get('name', 'N/A')}</p>
        <p><b>मूल्य:</b> ${coin.get('current_price', 0):.4f}</p>
    </body></html>
    """
    return subject, html

def send_decree_email(decision_data):
    """Sends a specific decree email based on the model's decision."""
    directive_type = decision_data.get("directive_type", "HOLD")
    print(f"Preparing to send '{directive_type}' decree email...")
    
    password = get_email_password()
    if not password:
        print("Could not send email: Password not available.")
        return

    if directive_type == "GENESIS":
        subject, html_body = _build_genesis_html(decision_data)
    else: # Default to HOLD
        subject, html_body = _build_hold_html(decision_data)

    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText("Please enable HTML to view this message.", 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ '{directive_type}' decree successfully sent to the Emperor.")
    except Exception as e:
        print(f"❌ Failed to send '{directive_type}' decree: {e}")
