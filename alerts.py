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
    """Google Secret Manager बाट इमेल पासवर्ड प्राप्त गर्दछ।"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{EMAIL_PASSWORD_SECRET_ID}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching email password: {e}")
        return None

def _build_html_template(title, body_html):
    """सबै इमेलहरूको लागि एउटा साझा HTML टेम्प्लेट बनाउँछ।"""
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333; }}
            .header {{ padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .directive-title-genesis {{ color: #4CAF50; }}
            .directive-title-sleeping-giant {{ color: #2196F3; }}
            .directive-title-black-swan {{ color: #f44336; }}
            .directive-title-hold {{ color: #FFC107; }}
            .directive-title-urgent {{ color: #f44336; font-weight: bold; }}
            h3 {{ color: #bb86fc; border-bottom: 2px solid #bb86fc; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #444; text-align: left; }}
            th {{ background-color: #333; }}
            .summary {{ background-color: #333; padding: 15px; border-left: 5px solid #bb86fc; margin-bottom: 20px; border-radius: 5px; }}
            a {{ color: #03dac6; text-decoration: none; }}
        </style>
    </head>
    <body><div class="container"><div class="header">{title}</div>{body_html}</div></body>
    </html>
    """

def _build_genesis_html(data):
    coin = data['coin_data']
    title = f"<h1 class='directive-title-genesis'>🔥 Omega Prime - जेनेसिस आदेश</h1>"
    body = f"""
        <p><b>Directive ID:</b> G-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)} | <b>Conviction Score: {data['conviction_score']:.2f}%</b></p>
        <h3>कार्यकारी सारांश (नेपाली):</h3>
        <div class="summary">
            <p>ओमेगा प्राइमको क्वान्टम ब्रेनले, <b>{coin.get('name', 'N/A')} ({coin.get('symbol', 'N/A').upper()})</b> लाई आजको सर्वोच्च-विश्वास "Genesis" अवसरको रूपमा चिन्हित गरेको छ। {data['summary']}</p>
        </div>
        <h3>💡 उत्प्रेरक र भविष्यको सम्भावना</h3>
        <table>
            <tr><td><b>कोर प्रविधि</b></td><td>{data.get('catalyst', {}).get('कोर प्रविधि', 'डाटा उपलब्ध छैन।')}</td></tr>
            <tr><td><b>साझेदारी</b></td><td>{data.get('catalyst', {}).get('साझेदारी', 'डाटा उपलब्ध छैन।')}</td></tr>
        </table>
        <h3>📝 रणनीतिक कार्यान्वयन योजना</h3>
        <table>
            <tr><td><b>Entry Zone</b></td><td>${coin.get('current_price', 0) * 0.95:.4f} - ${coin.get('current_price', 0) * 1.05:.4f}</td></tr>
            <tr><td><b>Stop-loss</b></td><td>${coin.get('current_price', 0) * 0.90:.4f}</td></tr>
        </table>
        <h3>🛒 तिम्रो मिशन (Your Mission)</h3>
        <table>
            <tr><td><b>Gate.io</b></td><td><a href="#">[Buy Here]</a></td></tr>
            <tr><td><b>Website</b></td><td><a href="#">[Visit Website]</a></td></tr>
        </table>
    """
    subject = f"🔥 Omega Genesis Directive | DNA Analysis: {coin.get('name', 'N/A')}"
    return subject, _build_html_template(title, body)

def _build_hold_html(data):
    coin = data['coin_data']
    title = f"<h1 class='directive-title-hold'>🔥 Omega Daily Summary | Hold Directive</h1>"
    body = f"<h3>मुख्य सन्देश:</h3><div class='summary'><p>{data['reason']}</p></div><h3>उत्कृष्ट, तर अपर्याप्त उम्मेदवार:</h3><p><b>नाम:</b> {coin.get('name', 'N/A')} (${coin.get('current_price', 0):.4f})</p>"
    subject = "🔥 Omega Daily Summary | Hold Directive & Market Intel"
    return subject, _build_html_template(title, body)

def _build_black_swan_html(data):
    coin = data['coin_data']
    title = f"<h1 class='directive-title-black-swan'>👁️ Omega Black Swan Directive</h1>"
    body = f"<h3>Anomaly Detected: {coin.get('name', 'N/A')}</h3><div class='summary'><p><b>{data['summary']}</b></p><p><b>Investment Thesis:</b> {data['thesis']}</p></div>"
    subject = f"👁️ Omega Black Swan Directive | Anomaly Detected: {coin.get('name', 'N/A')}"
    return subject, _build_html_template(title, body)

def send_decree_email(decision_data):
    directive_type = decision_data.get("directive_type", "HOLD")
    print(f"शाही लेखक: '{directive_type}' आदेशको लागि इमेल तयार गर्दै...")
    
    password = get_email_password()
    if not password:
        print("इमेल पठाउन सकिएन: पासवर्ड उपलब्ध छैन।")
        return

    handler_map = {
        "GENESIS": _build_genesis_html,
        "BLACK_SWAN": _build_black_swan_html,
        "HOLD": _build_hold_html
        # "SLEEPING_GIANT" and "URGENT" handlers will be added here later
    }
    
    # Get the correct handler or default to HOLD
    handler = handler_map.get(directive_type, _build_hold_html)
    subject, html_body = handler(decision_data)

    msg = MIMEMultipart('alternative')
    msg['From'] = f"Omega Prime <{EMAIL_SENDER}>"
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText("This is a Royal Decree from Omega Prime. Please enable HTML to view this message.", 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ '{directive_type}' आदेश सफलतापूर्वक सम्राटलाई पठाइयो।")
    except Exception as e:
        print(f"❌ '{directive_type}' आदेश पठाउन असफल: {e}")
