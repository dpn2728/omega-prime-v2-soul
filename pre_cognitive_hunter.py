# pre_cognitive_hunter.py (v1.4 - The Corrected Mandate)
import requests, logging, time, json
from database_manager import get_db_connection
from config import API_KEYS, MARKET_PARAMETERS

logger = logging.getLogger(__name__)
WATCHLIST_WALLETS = {"ethereum": {"Binance_7": "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8"}}

class PreCognitiveHunter:
    def __init__(self):
        self.session = requests.Session(); self.etherscan_key = API_KEYS.get("onchain_scanners", {}).get("ethereum"); self.api_endpoints = { "ethereum": "https://api.etherscan.io/api" }

    def _fetch_transactions(self, chain, address):
        params = {"module": "account", "action": "tokentx", "address": address, "page": 1, "offset": 200, "sort": "desc", "apikey": self.etherscan_key}
        try:
            response = self.session.get(self.api_endpoints[chain], params=params, timeout=45)
            response.raise_for_status(); data = response.json(); time.sleep(0.25)
            if isinstance(data.get("result"), str): return []
            return data.get("result", [])
        except Exception: return []

    def _save_signal_to_db(self, cursor, coin_id, meta_data):
        tx_hash = meta_data.get("transaction_hash")
        cursor.execute("SELECT id FROM signals WHERE meta_json LIKE ?", (f'%{tx_hash}%',))
        if cursor.fetchone(): return
        cursor.execute("INSERT INTO signals (coin_id, signal_type, meta_json, weight) VALUES (?, ?, ?, ?);", (coin_id, "wallet_flow", json.dumps(meta_data), 0.70))
        logger.info(f"🔥 नयाँ संकेत फेला पर्यो! सिक्का ID: {coin_id}")

    def hunt_for_wallet_flows(self):
        logger.info("शिकारी (v1.4) तैनाथ। सही आदेशपत्र सक्रिय।")
        conn = get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            for chain, wallets in WATCHLIST_WALLETS.items():
                for wallet_name, address in wallets.items():
                    transactions = self._fetch_transactions(chain, address)
                    for tx in transactions:
                        if not isinstance(tx, dict) or tx.get('to', '').lower() != address.lower(): continue
                        token_symbol = tx.get('tokenSymbol', '').upper(); token_name = tx.get('tokenName', ''); contract_addr = tx.get('contractAddress', '')
                        if not token_symbol or not token_name or not contract_addr: continue
                        
                        cursor.execute("SELECT id FROM coins WHERE contract_address = ?", (contract_addr,))
                        coin_row = cursor.fetchone()
                        
                        coin_id = None
                        if coin_row:
                            coin_id = coin_row['id']
                        else:
                            logger.info(f"अज्ञात सम्पत्ति '{token_name}' ({token_symbol}) फेला पर्यो। साम्राज्यमा दर्ता गर्दै...")
                            # --- समाधान: co_address को सट्टा contract_address प्रयोग गर्ने ---
                            cursor.execute("INSERT INTO coins (symbol, name, coingecko_id, contract_address, chain) VALUES (?, ?, ?, ?, ?)", (token_symbol, token_name, f"unknown_{contract_addr}", contract_addr, chain))
                            coin_id = cursor.lastrowid
                        
                        meta = { "source_wallet": wallet_name, "transaction_hash": tx.get('hash') }
                        self._save_signal_to_db(cursor, coin_id, meta)
            conn.commit()
        except Exception as e:
            logger.error(f"शिकार चक्रमा त्रुटि: {e}", exc_info=True)
        finally:
            if conn: conn.close()
