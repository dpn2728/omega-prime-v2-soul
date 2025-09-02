# sentinel_check.py (v1.0 - The Imperial Sentinel's Diagnostic)

import requests
import logging
from datetime import datetime, timedelta

# --- साम्राज्यका सम्बन्धित अंगहरूबाट जानकारी तान्ने ---
try:
    from config import API_KEYS
    # NOTE: We are importing the hunter's file itself to read its static variable
    from pre_cognitive_hunter import WATCHLIST_WALLETS
except Exception as e:
    print(f"FATAL: आवश्यक फाइलहरू (config.py, pre_cognitive_hunter.py) भेट्टाउन सकिएन: {e}")
    exit()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ImperialSentinel")

def run_diagnostics():
    """
    यो प्रोटोकलले हाम्रो शिकारीको आँखा (API Key) र शिकार स्थल (Wallet) को स्वास्थ्य जाँच गर्छ।
    """
    logger.info("="*50)
    logger.info("👑 अकाट्य निदान प्रोटोकल (v1.0) सुरु हुँदैछ...")
    logger.info("="*50)

    # --- १. शाही छापको परीक्षण (API Key Verification) ---
    etherscan_key = API_KEYS.get("onchain_scanners", {}).get("ethereum")
    if not etherscan_key or "YOUR_" in etherscan_key:
        logger.error("🛑 निदान असफल: `omega_secrets.py` मा ETHERSCAN_API_KEY सेट गरिएको छैन।")
        return

    logger.info(f"🔑 शाही छाप (API Key) को परीक्षण गर्दै: ...{etherscan_key[-4:]}")
    test_url = f"https://api.etherscan.io/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey={etherscan_key}"
    
    try:
        response = requests.get(test_url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "1":
            logger.info("✅ निदान सफल: शाही छाप (API Key) मान्य छ र Etherscan ले स्वीकार गर्यो।")
        else:
            logger.error(f"🛑 निदान असफल: Etherscan ले शाही छापलाई अस्वीकार गर्यो। सन्देश: {data.get('message')}")
            return
    except Exception as e:
        logger.error(f"🛑 निदान असफल: Etherscan सँग जडान हुन सकेन। त्रुटि: {e}")
        return

    # --- २. शिकार स्थलको परीक्षण (Wallet Activity Verification) ---
    if not WATCHLIST_WALLETS.get("ethereum"):
        logger.error("🛑 निदान असफल: `pre_cognitive_hunter.py` मा कुनै पनि Ethereum वालेट ठेगाना फेला परेन।")
        return

    for wallet_name, address in WATCHLIST_WALLETS["ethereum"].items():
        logger.info("-" * 50)
        logger.info(f"🎯 शिकार स्थलको परीक्षण गर्दै: {wallet_name} ({address})")

        # २(a). ERC-20 टोकन गतिविधि
        tokentx_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={etherscan_key}"
        # २(b). सामान्य ETH गतिविधि
        txlist_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={etherscan_key}"

        try:
            tokentx_data = requests.get(tokentx_url).json()
            txlist_data = requests.get(txlist_url).json()

            if isinstance(tokentx_data.get("result"), list):
                logger.info(f"    - ERC-20 टोकन स्थानान्तरण (हाम्रो हालको विधि): {len(tokentx_data['result'])} लेनदेनहरू फेला परे।")
            else:
                logger.warning(f"    - ERC-20 टोकन स्थानान्तरण: Etherscan बाट चेतावनी - {tokentx_data.get('message')}")

            if isinstance(txlist_data.get("result"), list):
                logger.info(f"    - सामान्य ETH स्थानान्तरण (भविष्यको विधि): {len(txlist_data['result'])} लेनदेनहरू फेला परे।")
            else:
                logger.warning(f"    - सामान्य ETH स्थानान्तरण: Etherscan बाट चेतावनी - {txlist_data.get('message')}")

        except Exception as e:
            logger.error(f"    - {wallet_name} को लागि गतिविधि जाँच गर्न असफल। त्रुटि: {e}")

    logger.info("=" * 50)
    logger.info("👑 निदान प्रोटोकल सम्पन्न भयो।")
    logger.info("=" * 50)

if __name__ == "__main__":
    run_diagnostics()
