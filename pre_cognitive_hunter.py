# pre_cognitive_hunter.py (v1.6 - The Coronation of the Hunter)
import requests, logging, time, json
from database_manager import get_db_connection
from config import API_KEYS, WATCHLIST_WALLETS

logger = logging.getLogger(__name__)

class PreCognitiveHunter:
    def __init__(self):
        self.session = requests.Session()
        self.etherscan_key = API_KEYS.get("onchain_scanners", {}).get("ethereum")
        self.api_endpoints = { "ethereum": "https://api.etherscan.io/api" }

    def _fetch_transactions(self, address):
        params = {"module": "account", "action": "tokentx", "address": address, "page": 1, "offset": 200, "sort": "desc", "apikey": self.etherscan_key}
        try:
            response = self.session.get(self.api_endpoints["ethereum"], params=params, timeout=45)
            response.raise_for_status(); data = response.json(); time.sleep(0.3)
            if isinstance(data.get("result"), str): return []
            return data.get("result", [])
        except Exception: return []

    def hunt_for_wallet_flows(self):
        logger.info("शिकारी (v1.6) तैनाथ। राज्याभिषेक आदेश सक्रिय।")
        conn = get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            for wallet_name, address in WATCHLIST_WALLETS.get("ethereum", {}).items():
                transactions = self._fetch_transactions(address)
                for tx in transactions:
                    if not isinstance(tx, dict) or tx.get('to','').lower() != address.lower(): continue
                    contract_addr = tx.get('contractAddress', ''); token_symbol = tx.get('tokenSymbol','').upper(); token_name = tx.get('tokenName','')
                    if not contract_addr or not token_symbol or not token_name: continue
                    
                    cursor.execute("SELECT id FROM coins WHERE contract_address = ?", (contract_addr,))
                    coin_row = cursor.fetchone()
                    coin_id = None
                    if coin_row:
                        coin_id = coin_row['id']
                    else:
                        # --- समाधान: अज्ञात नागरिकलाई साम्राज्यमा दर्ता गर्ने शाही अधिकार ---
                        logger.info(f"अज्ञात सम्पत्ति '{token_name}' ({token_symbol}) फेला पर्यो। साम्राज्यमा दर्ता गर्दै...")
                        cursor.execute("INSERT OR IGNORE INTO coins (symbol, name, coingecko_id, contract_address, chain) VALUES (?, ?, ?, ?, ?)", (token_symbol, token_name, f"unknown_{contract_addr}", contract_addr, "ethereum"))
                        coin_id = cursor.lastrowid
                    
                    if coin_id:
                        meta = { "source_wallet": wallet_name, "transaction_hash": tx.get('hash') }
                        cursor.execute("INSERT OR IGNORE INTO signals (coin_id, signal_type, meta_json, weight) VALUES (?, ?, ?, ?);", (coin_id, "wallet_flow", json.dumps(meta), 0.70))
                        logger.info(f"🔥 नयाँ संकेत फेला पर्यो! सिक्का ID: {coin_id} ({token_symbol})")
            conn.commit()
        except Exception as e:
            logger.error(f"शिकार चक्रमा त्रुटि: {e}", exc_info=True)
        finally:
            if conn: conn.close()
