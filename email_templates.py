# email_templates.py (v5.2 - The Oracle's Proclamation)

import datetime

def _get_confidence_color(value):
    """मानको आधारमा गतिशील रूपमा HTML रङ फर्काउँछ।"""
    if not isinstance(value, (int, float)): return "#e0e0e0"
    if value >= 85: return "#28a745" # Green
    if value >= 60: return "#ffc107" # Yellow
    return "#dc3545" # Red

def emperor_email_template(subject, content):
    """सबै शाही आदेशहरूको लागि अन्तिम र परिष्कृत HTML टेम्प्लेट।"""
    return f"""
    <!DOCTYPE html><html><head><title>{subject.split('|')[0]}</title><style>body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #0a0a0a; color: #e0e0e0; }} .container {{ max-width: 800px; margin: 20px auto; background-color: #121212; border-radius: 10px; overflow: hidden; border: 1px solid #333; }} .header {{ padding: 20px; text-align: center; background: linear-gradient(135deg, #d4af37 0%, #a07d20 100%); }} .header h1 {{ margin: 0; color: #121212; font-size: 24px; font-weight: bold; }} .content {{ padding: 25px; }} h3 {{ color: #d4af37; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 25px; font-size: 18px;}} table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }} th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; font-size: 14px; vertical-align: top; }} th {{ background-color: #1e1e1e; font-size: 14px; color: #d4af37; text-transform: uppercase; }} .footer {{ padding: 15px; text-align: center; font-size: 12px; color: #888; background-color: #0a0a0a; }} .button {{ background-color: #d4af37; color: #121212; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 5px; display: inline-block; }}</style></head><body><div class="container"><div class="header"><h1>{subject.split('|')[0]}</h1></div><div class="content">{content}</div><div class="footer"><p>OMEGA PRIME AI (v1000.0 - Oracle Engine) | The Emperor's Final Word</p></div></div></body></html>
    """

def generate_genesis_directive(coin_data):
    """
    "जेनेसिस डाइरेक्टिभ": अब वास्तविक, AI-उत्पन्न भविष्यवाणीहरू समावेश गर्दछ।
    """
    name = coin_data.get('name', 'N/A'); symbol = coin_data.get('symbol', 'N/A').upper()
    conviction = coin_data.get('conviction_score', 0)
    subject = f"🔥 Omega Prime Genesis Directive | Oracle AI: {name} ({symbol})"
    
    content = f"""
        <div style="text-align: center; font-size: 12px; color: #888; margin-bottom: 20px;">
            Directive ID: G-{datetime.now().strftime("%Y%m%d-%H%M")} | 
            Conviction Score: <b style="color:{_get_confidence_color(conviction)}; font-size: 14px;">{conviction:.1f}%</b>
        </div>
        <h3>१. कार्यकारी सारांश (Executive Summary):</h3><p>{coin_data.get('summary', 'डाटा उपलब्ध छैन')}</p>
        <h3>२. AI को आन्तरिक मोनोलग (AI's Internal Monologue):</h3><p style="border-left: 3px solid #d4af37; padding-left: 15px; font-style: italic; color: #aaa;">"{coin_data.get('ai_monologue', 'डाटा उपलब्ध छैन')}"</p>
        
        <!-- --- समाधान: "बहु-क्षितिज भविष्यवाणी" अब वास्तविक डाटा देखाउँछ --- -->
        <h3>३. बहु-क्षितिज भविष्यवाणी (Multi-Horizon Prediction):</h3>
        <table>
            <tr><th>समय-सीमा</th><th>AI पूर्वानुमानित लक्ष्य</th><th>विश्वास</th></tr>
            <tr><td><b>७ दिन</b></td><td><b>~${coin_data.get('pred_7d', 'N/A')}</b></td><td rowspan="3">{coin_data.get('confidence', 'N/A')}</td></tr>
            <tr><td><b>१४ दिन</b></td><td><b>~${coin_data.get('pred_14d', 'N/A')}</b></td></tr>
            <tr><td><b>३० दिन</b></td><td><b>~${coin_data.get('pred_30d', 'N/A')}</b></td></tr>
        </table>

        <h3>९. रणनीतिक कार्यान्वयन योजना (Actionable Strategy):</h3>
        <table>
            <tr><th>विश्लेषण</th><th>आदेश (Directive)</th></tr>
            <tr><td><b>प्रवेश निर्देशन</b></td><td><b>Optimal Zone: ${coin_data.get('entry_low', 'N/A')} - ${coin_data.get('entry_high', 'N/A')}</b></td></tr>
            <tr><td><b>जोखिम न्यूनीकरण</b></td><td><b>Hard stop-loss at ${coin_data.get('stop_loss', 'N/A')}. NO EXCEPTIONS.</b></td></tr>
        </table>
        
        <h3>१०. तिम्रो मिशन (Your Mission):</h3>
        <div style="text-align: center;">
             <a href="#" class="button">Gate.io</a>
             <a href="#" class="button">MEXC</a>
             <a href="#" class="button">Website</a>
        </div>
    """
    return subject, emperor_email_template(subject, content)

def generate_hold_directive(market_data):
    """'होल्ड डाइरेक्टिभ' को लागि टेम्प्लेट।"""
    subject = "🌙 Omega Daily Summary | Hold Directive & Market Intel"
    content = f"""
        <h3>रणनीतिक सारांश (Strategic Summary)</h3>
        <p>ओमेगाले आज कुनै पनि योग्य अवसर भेट्टाएन। आजको आदेश: <b>होल्ड / पूँजी संरक्षण</b>।</p>
        <p><i><b>उत्कृष्ट, तर अपर्याप्त उम्मेदवार:</b> {market_data.get('best_rejected', 'N/A')}</i></p>
        <h3>📈 बजारको पल्स (MARKET PULSE)</h3>
        <table>
            <tr><th>मापदण्ड</th><th>मान / स्थिति</th></tr>
            <tr><td><b>Fear & Greed Index</b></td><td>{market_data.get('fear_and_greed', 'N/A')}</td></tr>
            <tr><td><b>Bitcoin Dominance</b></td><td>{market_data.get('btc_dominance', 'N/A')}%</td></tr>
        </table>
        <p><b>अर्को स्क्यान:</b> लगभग {market_data.get('next_scan_hours', 8)} घण्टामा।</p>
    """
    return subject, emperor_email_template(subject, content)
