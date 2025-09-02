# config.py (v3.0 - The Grand Imperial Control Room - Fully Armed & Integrated)

import logging

# --- I. SECRET VAULT INTEGRATION ---
# This is the most critical line: It securely imports all keys and secrets
# from the treasure vault, making them available to the control room.
try:
    from omega_secrets import *
except ImportError:
    print("FATAL: The treasure vault 'omega_secrets.py' was not found.")
    print("The empire cannot function without its secrets. Please create it.")
    exit()

# --- II. SYSTEM CORE CONFIGURATION ---
# Defines the operational tempo and logging detail of the entire empire.
LOGGING_LEVEL = logging.INFO
# The number of hours the engine will sleep after a full cycle.
MAIN_LOOP_SLEEP_HOURS = 8

# --- III. API KEYS & CREDENTIALS (Organized for System Use) ---
# This dictionary structures all imported secrets for easy access by different modules.
API_KEYS = {
    # Foundational engines for price, volume, and market cap data.
    "market_data": {
        "coinmarketcap": COINMARKETCAP_API_KEY,
        "coingecko": COINGECKO_API_KEY,
    },
    # Tier 1 Intelligence: The primary, most powerful news source.
    "news_tier1_aggregators": {
        "cryptopanic": CRYPTO_PANIC_API_KEY,
    },
    # Tier 2 Intelligence: The rotating arsenal of backup news sources.
    "news_tier2_general": {
        "newsapi_org": NEWS_API_ORG_KEY,
        "gnews_io": GNEWS_IO_KEY,
        "newsdata_io": NEWSDATA_IO_KEY,
        "marketaux": MARKETAUX_API_KEY,
        "the_guardian": THE_GUARDIAN_API_KEY,
    },
    # Tier 3 Intelligence: Deep-cover agents for social sentiment (Future).
    "social_tier3": {
        "twitter_key": TWITTER_X_API_KEY,
        "twitter_secret": TWITTER_X_API_SECRET,
        "reddit_id": REDDIT_CLIENT_ID,
        "reddit_secret": REDDIT_CLIENT_SECRET,
    },
    # On-chain scanners for the Guardian Mind's security checks.
    "onchain_scanners": {
        "ethereum": ETHERSCAN_API_KEY,
        "bsc": BSCSCAN_API_KEY,
    },
    # Keys for the Emperor's Iron Fist (automated trading).
    "execution_exchanges": EXCHANGE_API_KEYS
}

# --- IV. "THE GOLDEN FILTER" PARAMETERS ---
# These are the core rules for the Genesis Hunt.
MARKET_PARAMETERS = {
    # Only analyze coins below this price.
    "max_coin_price": 2.00,
    # Minimum 24h trading volume to ensure liquidity.
    "min_volume_24h": 50000,
    # Minimum market cap to filter out dead coins.
    "min_market_cap": 100000
}

# --- V. "THE IMPERIAL HERALD" (Email Alerting System) ---
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": SENDER_EMAIL,
    "password": SENDER_PASSWORD,
    "default_recipient": RECIPIENT_EMAIL
}

# --- VI. "THE GUARDIAN" (System Health Monitor) ---
SYSTEM_MONITOR_CONFIG = {
    # How often the Guardian checks system health (in seconds).
    "interval_seconds": 300, # 5 minutes
    "cpu_crit_percent": 95.0,
    "mem_crit_percent": 90.0,
    "disk_crit_percent": 95.0,
    # If no heartbeat is received from main.py in this time, send an alert.
    "heartbeat_timeout_seconds": 3600 # 1 hour
}
