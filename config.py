# config.py (v2.0 - Omega Prime Central Control - Future-Proof & Fully Armed)

import logging
import os

# --- I. SECURELY LOAD THE ENTIRE TREASURE VAULT ---
# This section securely imports every secret from the vault.
try:
    from omega_secrets import (
        # Section I: Alerting
        SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL,
        # Section II: Market Data
        COINMARKETCAP_API_KEY, CRYPTOCOMPARE_API_KEY,
        # Section III: News Engine
        NEWS_API_KEYS,
        # Section IV: On-Chain Eye
        ONCHAIN_API_KEYS,
        # Section V: Iron Fist (Execution)
        EXCHANGE_API_KEYS,
        # Section VI: Advanced DeFi
        DEFI_LAMA_API_KEY, DUNE_API_KEY, NANSEN_API_KEY, GLASSNODE_API_KEY,
        # Section VII: Social Sentiment & Dev Activity
        TWITTER_API_BEARER_TOKEN, REDDIT_API_CLIENT_ID, REDDIT_API_CLIENT_SECRET, GITHUB_PERSONAL_ACCESS_TOKEN,
        # Section VIII: Alternative Data & Notifications
        COINGECKO_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DISCORD_WEBHOOK_URL
    )
    SECRETS_LOADED = True
except ImportError:
    print("CRITICAL ERROR: 'omega_secrets.py' not found or is incomplete. The system cannot operate without its secrets.")
    SECRETS_LOADED = False
    # Create dummy values for all variables to prevent crashes
    SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL = None, None, None
    COINMARKETCAP_API_KEY, CRYPTOCOMPARE_API_KEY = None, None
    NEWS_API_KEYS, ONCHAIN_API_KEYS, EXCHANGE_API_KEYS = {}, {}, {}
    DEFI_LAMA_API_KEY, DUNE_API_KEY, NANSEN_API_KEY, GLASSNODE_API_KEY = None, None, None, None
    TWITTER_API_BEARER_TOKEN, REDDIT_API_CLIENT_ID, REDDIT_API_CLIENT_SECRET, GITHUB_PERSONAL_ACCESS_TOKEN = None, None, None, None
    COINGECKO_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DISCORD_WEBHOOK_URL = None, None, None, None

# --- II. CENTRAL API KEY REPOSITORY ---
# A single, organized dictionary for all modules to access any API key.
API_KEYS = {
    "market_data": {
        "coinmarketcap": COINMARKETCAP_API_KEY,
        "cryptocompare": CRYPTOCOMPARE_API_KEY,
        "coingecko": COINGECKO_API_KEY,
    },
    "news": NEWS_API_KEYS,
    "onchain": {
        "scanners": ONCHAIN_API_KEYS,
        "advanced_defi": {
            "dune": DUNE_API_KEY,
            "nansen": NANSEN_API_KEY,
            "glassnode": GLASSNODE_API_KEY,
        }
    },
    "social_dev": {
        "twitter_bearer": TWITTER_API_BEARER_TOKEN,
        "reddit_id": REDDIT_API_CLIENT_ID,
        "reddit_secret": REDDIT_API_CLIENT_SECRET,
        "github_token": GITHUB_PERSONAL_ACCESS_TOKEN,
    },
    "execution": EXCHANGE_API_KEYS
}

# --- III. SERVICE-SPECIFIC CONFIGURATIONS ---

# Email System Configuration
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com", "smtp_port": 587,
    "username": SENDER_EMAIL, "password": SENDER_PASSWORD,
    "default_recipient": RECIPIENT_EMAIL
}

# Execution Engine Configuration ("The Iron Fist")
EXECUTION_CONFIG = {
    "default_exchange": "kucoin",      # CRITICAL: The exchange to use for trades (must match a key in EXCHANGE_API_KEYS)
    "simulation_mode": True,           # CRITICAL: Set to False ONLY for LIVE TRADING
    "trade_amount_usdt": 10.0          # Default amount in USDT for each automated trade
}

# Advanced Notifications Configuration (Future Use)
NOTIFICATION_CONFIG = {
    "telegram_bot_token": TELEGRAM_BOT_TOKEN,
    "telegram_chat_id": TELEGRAM_CHAT_ID,
    "discord_webhook_url": DISCORD_WEBHOOK_URL,
}

# --- IV. LOGGING CONFIGURATION ---
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

def get_logger_config():
    return {
        'level': logging.INFO,
        'format': '%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s',
        'log_file': os.path.join(LOG_DIR, 'omega_prime_master.log'),
        'error_log_file': os.path.join(LOG_DIR, 'omega_prime_error.log'),
    }

# --- V. SYSTEM & DATA PARAMETERS ---
MARKET_PARAMETERS = {
    "max_coin_price": 0.50,
    "min_volume_24h": 50000,
    "min_market_cap": 100000
}

# --- VI. SYSTEM HEALTH CHECK ---
def is_configured_correctly():
    """Checks if all CRITICAL secrets and configurations are loaded."""
    if not SECRETS_LOADED:
        logging.critical("System HALTED. 'omega_secrets.py' is missing or corrupted.")
        return False
    
    # Check for the absolute minimum requirements to run
    if not API_KEYS["market_data"]["coinmarketcap"]:
        logging.critical("System HALTED. CoinMarketCap API key is missing.")
        return False
    if not EMAIL_CONFIG["username"] or not EMAIL_CONFIG["password"]:
        logging.critical("System HALTED. Email credentials are not configured.")
        return False
        
    logging.info("Configuration and secrets loaded successfully. System is armed and ready.")
    return True
