# config.py (v3.2 - The Supreme Imperial Control Room)

import logging

# --- I. शाही खजाना भण्डारसँग एकीकरण ---
# यसले 'omega_secrets.py' बाट सबै गोप्य कुञ्जीहरूलाई सुरक्षित रूपमा लोड गर्छ।
try:
    from omega_secrets import *
except ImportError:
    print("FATAL: शाही खजाना भण्डार 'omega_secrets.py' फेला परेन।")
    exit()

# --- II. साम्राज्यको कोर कन्फिगरेसन ---
# समाधान: सर्वोच्च कमाण्डरले खोज्ने सही नाम।
LOGGING_LEVEL = logging.INFO
# हरेक शिकार चक्र पछि साम्राज्यले आराम गर्ने घण्टा।
MAIN_LOOP_SLEEP_HOURS = 8

# --- III. "सुनौलो फिल्टर" को शाही नियम ---
# यी नियमहरूले "जेनेसिस" शिकारको लागि आधारभूत मापदण्ड निर्धारण गर्छन्।
MARKET_PARAMETERS = {
    "max_coin_price": 2.00,
    "min_volume_24h": 50000,
    "min_market_cap": 100000
}

# --- IV. शाही हतियारहरूको रणनीतिक संगठन ---
# 'omega_secrets.py' बाट सबै API कुञ्जीहरूलाई व्यवस्थित गर्ने।
API_KEYS = {
    "tier1_intelligence": {
        "cryptopanic": CRYPTO_PANIC_API_KEY,
        "coingecko": COINGECKO_API_KEY,
    },
    "tier2_intelligence": {
        "newsapi_org": NEWS_API_ORG_KEY,
        "gnews_io": GNEWS_IO_KEY,
        "newsdata_io": NEWSDATA_IO_KEY,
        "marketaux": MARKETAUX_API_KEY,
        "the_guardian": THE_GUARDIAN_API_KEY,
    },
    "tier3_intelligence": {
        "twitter_key": TWITTER_X_API_KEY,
        "twitter_secret": TWITTER_X_API_SECRET,
        "reddit_id": REDDIT_CLIENT_ID,
        "reddit_secret": REDDIT_CLIENT_SECRET,
    },
    "market_data": {
        "coinmarketcap": COINMARKETCAP_API_KEY,
        "cryptocompare": CRYPTOCOMPARE_API_KEY,
    },
    "onchain_scanners": {
        "ethereum": ETHERSCAN_API_KEY,
        "bsc": BSCSCAN_API_KEY,
        "polygon": POLYGONSCAN_API_KEY,
    }
}

# --- V. पूर्व-संज्ञानात्मक शिकारीको लक्ष्य ---
# केन्द्रीय नियन्त्रण कक्षबाट शिकारीको लागि लक्ष्यहरू निर्धारण गर्ने।
WATCHLIST_WALLETS = {
    "ethereum": {
        "Binance_7": "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8",
        "Binance_Hot_Wallet_20": "0xf977814e90da44bfa03b6295a0616a897441acec",
    }
    # भविष्यमा यहाँ BSC, Polygon आदिको लागि लक्ष्यहरू थप्न सकिन्छ
}

# --- VI. शाही उद्घोषकको कन्फिगरेसन ---
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": SENDER_EMAIL,
    "password": SENDER_PASSWORD,
    "default_recipient": RECIPIENT_EMAIL
}
