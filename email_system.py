# email_system.py (v1.0 - The Imperial Herald)

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- केन्द्रीय नियन्त्रण कक्षबाट कन्फिगरेसन लोड गर्ने ---
try:
    from config import EMAIL_CONFIG
except ImportError:
    print("FATAL: `config.py` not found. The Imperial Herald cannot speak.")
    EMAIL_CONFIG = {}

class EmailService:
    """
    उद्देश्य #31-35: Omega Prime को लागि इमेल पठाउने सेवा।
    यो "शाही उद्घोषक" हो जसले AI को निष्कर्षहरू सम्राटलाई पठाउँछ।
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Singleton Pattern: __init__ एक पटक मात्र चल्छ
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = EMAIL_CONFIG
        
        # कन्फिगरेसन जाँच
        if not all([self.config.get('smtp_server'), self.config.get('smtp_port'), 
                    self.config.get('username'), self.config.get('password')]):
            self.logger.critical("इमेल कन्फिगरेसन अपूर्ण छ। शाही उद्घोषक मौन छ।")
            self.is_configured = False
        else:
            self.is_configured = True
            self.logger.info("शाही उद्घोषक (v1.0) अनलाइन आयो र आदेश पठाउन तयार छ।")

    def send_html_email(self, recipient, subject, html_body):
        """
        एउटा HTML इमेल पठाउने मुख्य प्रकार्य।
        :param recipient: प्राप्तकर्ताको इमेल ठेगाना।
        :param subject: इमेलको विषय।
        :param html_body: इमेलको HTML सामग्री।
        :return: bool: True यदि सफल भयो, अन्यथा False।
        """
        if not self.is_configured:
            self.logger.error("इमेल पठाउन सकिएन किनभने प्रणाली कन्फिगर गरिएको छैन।")
            return False

        msg = MIMEMultipart('alternative')
        msg['From'] = self.config['username']
        msg['To'] = recipient
        msg['Subject'] = subject

        # HTML सामग्री संलग्न गर्ने
        msg.attach(MIMEText(html_body, 'html'))

        try:
            self.logger.info(f"'{subject}' विषयको साथ '{recipient}' लाई शाही आदेश पठाउँदै...")
            # Gmail SMTP सर्भरसँग सुरक्षित जडान स्थापना गर्ने
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()  # जडान सुरक्षित गर्ने
                server.login(self.config['username'], self.config['password'])
                server.send_message(msg)
            self.logger.info("आदेश सफलतापूर्वक पठाइयो।")
            return True
        except smtplib.SMTPAuthenticationError:
            self.logger.critical("FATAL: SMTP प्रमाणीकरण असफल भयो! `omega_secrets.py` मा SENDER_EMAIL/SENDER_PASSWORD जाँच गर्नुहोस्। 'Less secure app access' वा 'App Password' आवश्यक हुन सक्छ।")
            return False
        except Exception as e:
            self.logger.error(f"शाही आदेश पठाउँदा त्रुटि: {e}", exc_info=True)
            return False

# --- `main.py` द्वारा प्रयोग गरिने मुख्य प्रकार्य ---
def send_directive_email(subject, html_body):
    """
    `main.py` बाट सजिलैसँग कल गर्न मिल्ने एक विश्वव्यापी प्रकार्य।
    यसले EmailService को एकल उदाहरण (singleton) प्रयोग गर्दछ।
    """
    herald = EmailService()
    recipient = herald.config.get('default_recipient', 'default@example.com')
    return herald.send_html_email(recipient, subject, html_body)

# --- आत्म-परीक्षण ब्लक ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    herald = EmailService()
    if herald.is_configured:
        print("शाही उद्घोषकको परीक्षण चलिरहेको छ...")
        test_subject = "🛡️ OMEGA PRIME HERALD TEST"
        test_body = """
        <html>
        <body>
            <h1>This is a test directive.</h1>
            <p>If you receive this, the Imperial Herald is functioning correctly.</p>
            <p style="color: green; font-weight: bold;">System Online.</p>
        </body>
        </html>
        """
        recipient_email = herald.config.get('default_recipient')
        if recipient_email:
            success = herald.send_html_email(recipient_email, test_subject, test_body)
            if success:
                print(f"परीक्षण इमेल सफलतापूर्वक '{recipient_email}' मा पठाइयो।")
            else:
                print(f"परीक्षण इमेल पठाउन असफल। कृपया लगहरू जाँच गर्नुहोस्।")
        else:
            print("त्रुटि: `config.py` मा 'default_recipient' सेट गरिएको छैन।")
    else:
        print("परीक्षण रद्द गरियो किनभने इमेल प्रणाली कन्फिगर गरिएको छैन।")
