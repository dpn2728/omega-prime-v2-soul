# email_templates.py (v1.1 - The Imperial Herald with Dynamic Timing - FINAL)

import datetime

# --- I. HELPER FUNCTIONS AND CONSTANTS (सहयोगी कार्यहरू र स्थिर मानहरू) ---

EXCHANGE_LINKS = {
    'kucoin': 'https://www.kucoin.com/trade/{}_USDT',
    'gateio': 'https://www.gate.io/trade/{}_USDT',
    'mexc': 'https://www.mexc.com/exchange/{}_USDT',
    'uniswap': 'https://app.uniswap.org/swap?outputCurrency={}'
}

def generate_exchange_links(symbol, contract_address=None):
    """दिइएको सिक्काको लागि गतिशील रूपमा एक्सचेन्ज लिङ्कहरू उत्पन्न गर्दछ।"""
    links = {}
    upper_symbol = symbol.upper() if symbol else ''
    for exchange, template in EXCHANGE_LINKS.items():
        if exchange == 'uniswap' and contract_address:
            links[exchange] = template.format(contract_address)
        elif exchange != 'uniswap' and symbol:
            links[exchange] = template.format(upper_symbol)
    return links

def get_risk_html(risk_name, risk_value):
    """जोखिमको मान अनुसार HTML रङ प्रदान गर्दछ।"""
    if risk_value is None: return f"<li><b>{risk_name}:</b> Not Assessed</li>"
    color = "#ffc107" # Medium (default)
    if risk_value <= 3: color = "#28a745" # Low
    if risk_value >= 7: color = "#dc3545" # High
    return f'<li><b>{risk_name}:</b> <span style="color: {color}; font-weight: bold;">{risk_value}/10</span></li>'

def modern_email_template(subject, content):
    """सबै इमेलहरूको लागि एक आधुनिक र व्यावसायिक HTML टेम्प्लेट।"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{subject}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #0a0a0a; color: #e0e0e0; }}
            .container {{ max-width: 800px; margin: 20px auto; background-color: #121212; border-radius: 10px; overflow: hidden; border: 1px solid #333; }}
            .header {{ padding: 20px; text-align: center; background: linear-gradient(135deg, #d4af37 0%, #a07d20 100%); }}
            .header h1 {{ margin: 0; color: #121212; font-size: 28px; font-weight: bold; }}
            .content {{ padding: 25px; }}
            h2 {{ color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 5px; margin-top: 30px; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ margin-bottom: 10px; background-color: #1e1e1e; padding: 10px; border-radius: 5px; }}
            .footer {{ padding: 15px; text-align: center; font-size: 12px; color: #888; background-color: #1e1e1e; }}
            a {{ color: #d4af37; text-decoration: none; }}
            .button {{ background-color: #d4af37; color: #121212; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>{subject}</h1></div>
            <div class="content">{content}</div>
            <div class="footer">
                <p>OMEGA PRIME AI | The Emperor's Eye on the Crypto Universe</p>
                <p>This is an automated directive. Do your own research.</p>
            </div>
        </div>
    </body>
    </html>
    """

# --- II. MAIN EMAIL GENERATION FUNCTIONS (मुख्य इमेल उत्पादन कार्यहरू) ---

def generate_genesis_directive(coin_data, tri_mind_approval):
    """अद्यावधिक 'जेनेसिस डाइरेक्टिभ', जसमा त्रि-मस्तिष्क सहमति, विस्तृत जोखिम, र स्मार्ट मनी विश्लेषण समावेश छ।"""
    if not all(tri_mind_approval.values()):
        return None, "Tri-Mind consensus not reached. Directive aborted."
    
    coin_name = coin_data.get('name', 'N/A')
    symbol = coin_data.get('symbol', 'N/A')
    subject = f"🔥 OMEGA PRIME GENESIS DIRECTIVE: {coin_name} ({symbol})"
    
    exchange_links = generate_exchange_links(symbol, coin_data.get('contract_address'))
    
    content = f"""
        <p style="text-align: center; font-size: 12px; color: #888;">
            Directive ID: {coin_data.get('id', 'N/A')} | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
        </p>

        <h2>🎯 EXECUTIVE SUMMARY</h2>
        <p>{coin_data.get('summary', 'No summary available.')}</p>

        <h2>✅ TRI-MIND CONSENSUS</h2>
        <ul>
            <li><b>Prophet (Predictive AI):</b> ✅ Approved (Confidence: {coin_data.get('prophet_confidence', 0)}%)</li>
            <li><b>Strategist (Risk & Reward AI):</b> ✅ Approved (Confidence: {coin_data.get('strategist_confidence', 0)}%)</li>
            <li><b>Guardian (Security & Anomaly AI):</b> ✅ Approved (Confidence: {coin_data.get('guardian_confidence', 0)}%)</li>
        </ul>

        <h2>📈 CORE ANALYSIS</h2>
        <ul>
            <li><b>Price:</b> ${coin_data.get('price', 0):,.8f}</li>
            <li><b>Market Cap:</b> ${coin_data.get('market_cap', 0):,.0f}</li>
            <li><b>Volume (24h):</b> ${coin_data.get('volume', 0):,.0f}</li>
            <li><b>Exchange Status:</b> {coin_data.get('exchange_status', 'Not listed on Top-5')}</li>
        </ul>
        
        <h2>🛡️ DETAILED RISK ASSESSMENT</h2>
        <ul>
            {get_risk_html('Liquidity Risk', coin_data.get('liquidity_risk'))}
            {get_risk_html('Volatility Risk', coin_data.get('volatility_risk'))}
            {get_risk_html('Smart Contract Risk', coin_data.get('contract_risk'))}
            {get_risk_html('Regulatory Risk', coin_data.get('regulatory_risk'))}
        </ul>
        
        <h2>📅 PRICE PREDICTIONS (AI-DRIVEN)</h2>
        <ul>
            <li><b>1-Day Horizon:</b> {coin_data.get('pred_1d', 'N/A')} (Confidence: {coin_data.get('conf_1d', 0)}%)</li>
            <li><b>7-Day Horizon:</b> {coin_data.get('pred_7d', 'N/A')} (Confidence: {coin_data.get('conf_7d', 0)}%)</li>
            <li><b>30-Day Horizon:</b> {coin_data.get('pred_30d', 'N/A')} (Confidence: {coin_data.get('conf_30d', 0)}%)</li>
        </ul>
        
        <h2>⚡ ACTION PLAN</h2>
        <ul>
            <li><b>Entry Zone:</b> ${coin_data.get('entry_low', 'N/A')} - ${coin_data.get('entry_high', 'N/A')}</li>
            <li><b>Stop-Loss:</b> ${coin_data.get('sl', 'N/A')}</li>
            <li><b>Portfolio Allocation:</b> {coin_data.get('allocation', 'N/A')}%</li>
        </ul>
        
        <h2>🔗 EXECUTION & RESEARCH LINKS</h2>
        <div style="text-align: center;">
            {'<a href="' + exchange_links['kucoin'] + '" class="button">Buy on KuCoin</a>' if 'kucoin' in exchange_links else ''}
            {'<a href="' + exchange_links['gateio'] + '" class="button">Buy on Gate.io</a>' if 'gateio' in exchange_links else ''}
            {'<a href="' + exchange_links['mexc'] + '" class="button">Buy on MEXC</a>' if 'mexc' in exchange_links else ''}
            {'<a href="' + exchange_links['uniswap'] + '" class="button">Buy on Uniswap</a>' if 'uniswap' in exchange_links else ''}
            <br/><br/>
            <a href="{coin_data.get('website', '#')}">Website</a> | 
            <a href="{coin_data.get('whitepaper', '#')}">Whitepaper</a> | 
            <a href="{coin_data.get('explorer', '#')}">Explorer</a>
        </div>
    """
    return subject, modern_email_template(subject, content)

def generate_hold_directive(market_data, next_scan_interval_hours):
    """
    (v1.1) 'होल्ड डाइरेक्टिभ' को लागि अद्यावधिक टेम्प्लेट।
    अब यसले `main.py` बाट अर्को स्क्यानको सही समय लिन्छ।
    """
    subject = "🌙 OMEGA PRIME HOLD DIRECTIVE"
    content = f"""
        <h2>STATUS: NO HIGH-PROBABILITY OPPORTUNITIES DETECTED</h2>
        <p>Patience is a key virtue in trading. Today, the optimal strategy is to wait for a clearer, high-probability setup. We continue to scan the universe for the next Genesis candidate.</p>
        
        <h2>📈 CURRENT MARKET ANALYSIS</h2>
        <ul>
            <li><b>Market State:</b> {market_data.get('state', 'Consolidating')}</li>
            <li><b>Recommended Action:</b> {market_data.get('action', 'Hold positions and preserve capital.')}</li>
            <li><b>Next Scan:</b> In {next_scan_interval_hours} hours.</li>
        </ul>
    """
    return subject, modern_email_template(subject, content)

# Note: Other directive templates like Accelerate, Fortify, Imperial can be added here
# in the future using the same modern_email_template structure.
