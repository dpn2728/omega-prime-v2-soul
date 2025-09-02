# email_templates.py (v5.1 - The Emperor's Edict, Sealed and Final)

import datetime

# --- I. HELPER FUNCTIONS & STYLING (सहयोगी कार्यहरू र शैली) ---

def _get_confidence_color(value, high_is_good=True):
    """मानको आधारमा गतिशील रूपमा HTML रङ फर्काउँछ।"""
    if not isinstance(value, (int, float)): return "#e0e0e0"
    
    if high_is_good:
        if value >= 85: return "#28a745" # Green
        if value >= 60: return "#ffc107" # Yellow
        return "#dc3545" # Red
    else: # Low is good (e.g., risk score)
        if value <= 3: return "#28a745"
        if value <= 6: return "#ffc107"
        return "#dc3545"

def emperor_email_template(subject, content, version="v5.1"):
    """सबै शाही आदेशहरूको लागि अन्तिम र परिष्कृत HTML टेम्प्लेट।"""
    return f"""
    <!DOCTYPE html><html><head><title>{subject.split('|')[0]}</title><style>body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #0a0a0a; color: #e0e0e0; }} .container {{ max-width: 800px; margin: 20px auto; background-color: #121212; border-radius: 10px; overflow: hidden; border: 1px solid #333; }} .header {{ padding: 20px; text-align: center; background: linear-gradient(135deg, #d4af37 0%, #a07d20 100%); }} .header h1 {{ margin: 0; color: #121212; font-size: 24px; font-weight: bold; }} .content {{ padding: 25px; }} h3 {{ color: #d4af37; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 25px; font-size: 18px;}} table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }} th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; font-size: 14px; vertical-align: top; }} th {{ background-color: #1e1e1e; font-size: 14px; color: #d4af37; text-transform: uppercase; }} .footer {{ padding: 15px; text-align: center; font-size: 12px; color: #888; background-color: #0a0a0a; }} a {{ color: #d4af37; text-decoration: none; }} .button {{ background-color: #d4af37; color: #121212; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 5px; display: inline-block; }}</style></head><body><div class="container"><div class="header"><h1>{subject.split('|')[0]}</h1></div><div class="content">{content}</div><div class="footer"><p>OMEGA PRIME AI ({version}) | The Emperor's Final Word</p><p>This is an automated directive. Always conduct your own research.</p></div></div></body></html>
    """

def _generate_full_spectrum_body(coin_data):
    """
    सबै आक्रामक आदेशहरूको लागि केन्द्रीय "सम्राटको युद्ध योजना" खण्ड उत्पन्न गर्दछ।
    यो प्रकार्यले सबै ५ आदेशहरूमा एकरूपता र पूर्णता सुनिश्चित गर्दछ।
    """
    conviction = coin_data.get('conviction_score', 0)
    return f"""
        <div style="text-align: center; font-size: 12px; color: #888; margin-bottom: 20px;">
            Directive ID: G-{datetime.datetime.now().strftime("%Y%m%d-%H%M")} | 
            Conviction Score: <b style="color:{_get_confidence_color(conviction)}; font-size: 14px;">{conviction:.1f}%</b>
        </div>
        <h3>१. कार्यकारी सारांश (Executive Summary):</h3><p>{coin_data.get('summary', 'डाटा उपलब्ध छैन')}</p>
        <h3>२. AI को आन्तरिक मोनोलग (AI's Internal Monologue):</h3><p style="border-left: 3px solid #d4af37; padding-left: 15px; font-style: italic; color: #aaa;">"{coin_data.get('ai_monologue', 'डाटा उपलब्ध छैन')}"</p>
        <h3>३. बहु-क्षितिज भविष्यवाणी (Multi-Horizon Prediction):</h3><table><tr><th>समय-सीमा</th><th>मूल्य वृद्धि सम्भावना (>25%)</th><th>पूर्वानुमानित लक्ष्य</th></tr><tr><td><b>७ दिन</b></td><td style="color:{_get_confidence_color(coin_data.get('pred_prob_7d'))};"><b>{coin_data.get('pred_prob_7d', 'N/A')}%</b></td><td><b>~${coin_data.get('pred_target_7d', 'N/A')}</b></td></tr></table>
        <h3>४. उत्प्रेरक विश्लेषण (Catalyst & Pre-Cognitive Signals):</h3><table><tr><th>सङ्केतको स्रोत</th><th>विश्लेषण</th><th>विश्वास</th></tr><tr><td><b>भविष्यवक्ता आँखा</b></td><td>Mempool: {coin_data.get('mempool_signal', 'डाटा उपलब्ध छैन')}</td><td style="color:{_get_confidence_color(coin_data.get('mempool_confidence'))};"><b>{coin_data.get('mempool_confidence', 'N/A')}%</b></td></tr><tr><td><b>शिकारीको पदचाप</b></td><td>Smart Money: {coin_data.get('smart_money_signal', 'डाटा उपलब्ध छैन')}</td><td style="color:{_get_confidence_color(coin_data.get('smart_money_confidence'))};"><b>{coin_data.get('smart_money_confidence', 'N/A')}%</b></td></tr></table>
        <h3>८. शाही जोखिम म्याट्रिक्स (The Imperial Risk Matrix):</h3><table><tr><th>जोखिमको प्रकार</th><th>जोखिम स्तर (1-10)</th><th>सारांश</th></tr><tr><td><b>तरलता</b></td><td style="color:{_get_confidence_color(coin_data.get('risk_liquidity'), False)};"><b>{coin_data.get('risk_liquidity', 'N/A')}</b></td><td>{coin_data.get('risk_liquidity_summary', 'N/A')}</td></tr><tr><td><b>अस्थिरता</b></td><td style="color:{_get_confidence_color(coin_data.get('risk_volatility'), False)};"><b>{coin_data.get('risk_volatility', 'N/A')}</b></td><td>{coin_data.get('risk_volatility_summary', 'N/A')}</td></tr></table>
        <h3>९. रणनीतिक कार्यान्वयन योजना (Actionable Strategy):</h3><table><tr><th>विश्लेषण</th><th>आदेश (Directive)</th></tr><tr><td><b>प्रवेश निर्देशन</b></td><td><b>Optimal Zone: ${coin_data.get('entry_low', 'N/A')} - ${coin_data.get('entry_high', 'N/A')}</b></td></tr><tr><td><b>जोखिम न्यूनीकरण</b></td><td><b>Hard stop-loss at ${coin_data.get('stop_loss', 'N/A')}. NO EXCEPTIONS.</b></td></tr></table>
        <h3>१०. तिम्रो मिशन (Your Mission):</h3><div style="text-align: center;"><a href="{coin_data.get('gateio_link', '#')}" class="button">Gate.io</a><a href="{coin_data.get('mexc_link', '#')}" class="button">MEXC</a><a href="{coin_data.get('website', '#')}" class="button">Website</a></div>
    """

# --- II. THE 5 ROYAL DECREES (५ शाही आदेशहरू) ---

def generate_genesis_directive(coin_data):
    name = coin_data.get('name', 'N/A'); symbol = coin_data.get('symbol', 'N/A').upper()
    subject = f"🔥 Omega Prime Genesis Directive | Emperor's Battle Plan: {name} ({symbol})"
    header = f"<h3>Investment Thesis</h3><p><b>Front-run a near-certain Tier-1 exchange listing, driven by god-tier fundamentals and verifiable pre-cognitive signals.</b></p>"
    body = _generate_full_spectrum_body(coin_data)
    return subject, emperor_email_template(subject, header + body)

def generate_hold_directive(market_data):
    subject = "🌙 Omega Daily Summary | Hold Directive & Market Intel"
    content = f"<h3>रणनीतिक सारांश (Strategic Summary)</h3><p>ओमेगाले आज कुनै पनि योग्य अवसर भेट्टाएन। आजको आदेश: <b>होल्ड / पूँजी संरक्षण</b>। गलत युद्धमा प्रवेश नगर्नु पनि एक विजय हो।</p><p><i><b>उत्कृष्ट, तर अपर्याप्त उम्मेदवार:</b> {market_data.get('best_rejected', 'आज कुनै पनि सिक्का नजिक आएन।')}</i></p><h3>📈 बजारको पल्स (MARKET PULSE)</h3><table><tr><th>मापदण्ड</th><th>मान / स्थिति</th></tr><tr><td><b>Fear & Greed Index</b></td><td>{market_data.get('fear_and_greed', 'N/A')}</td></tr><tr><td><b>Bitcoin Dominance</b></td><td>{market_data.get('btc_dominance', 'N/A')}%</td></tr></table><p><b>अर्को स्क्यान:</b> लगभग {market_data.get('next_scan_hours', 8)} घण्टामा।</p>"
    return subject, emperor_email_template(subject, content)

def generate_sleeping_giant_directive(coin_data):
    name = coin_data.get('name', 'N/A')
    subject = f"🌟 Omega Contingency Directive | Sleeping Giant: {name}"
    header = f"<h2 style='color: #6c757d;'>आकस्मिक योजना सक्रिय</h2><h3>Investment Thesis</h3><p><b>A long-term (6-12 months) value investment before the market wakes up. The catalyst is not imminent, but the value is immense.</b></p>"
    body = _generate_full_spectrum_body(coin_data)
    return subject, emperor_email_template(subject, header + body)

def generate_black_swan_directive(coin_data):
    name = coin_data.get('name', 'N/A')
    subject = f"👁️ Omega Black Swan Directive | Anomaly Detected: {name}"
    header = f"<h2 style='color: #dc3545;'>चेतावनी: उच्च-जोखिम, उच्च-प्रतिफल</h2><h3>Investment Thesis</h3><p><b>A calculated gamble on a potential paradigm shift. Max Allocation: <span style='color:#dc3545;'>0.5%</span> of portfolio.</b></p>"
    body = _generate_full_spectrum_body(coin_data)
    return subject, emperor_email_template(subject, header + body)

def generate_urgent_alpha_alert(coin_data):
    name = coin_data.get('name', 'N/A')
    subject = f"🔴 URGENT | Pre-Listing Anomaly Detected: {name}"
    header = f"<h2 style='color: #ffc107;'>तत्काल कारबाही आवश्यक</h2><p>ओमेगाले अकाट्य, समय-संवेदनशील घटना देखेको छ: <b>{coin_data.get('urgent_signal', 'Listing on a major exchange is imminent.')}</b></p><p><b>विश्वास: <span style='color:#28a745;'>99%+</span> | समय-सीमा: <span style='color:#dc3545;'>अनुमानित ४ घण्टाभित्र</span></b></p><h3>Investment Thesis</h3><p><b>Execute immediately via DEX to front-run the imminent CEX listing announcement.</b></p>"
    body = _generate_full_spectrum_body(coin_data)
    return subject, emperor_email_template(subject, header + body)
