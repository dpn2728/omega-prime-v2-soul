# market_cmc.py (Final Version - Renamed Secrets)

import logging
from typing import Optional, List, Dict, Any
from requests import Session, exceptions

# --- THIS IS THE FIX: Import from the renamed secrets file ---
from omega_secrets import COINMARKETCAP_API_KEY

class CMCAPIError(Exception):
    """Custom exception for CoinMarketCap API errors."""
    pass

class CMCSense:
    def __init__(self):
        self.api_url = 'https://pro-api.coinmarketcap.com'
        self.logger = logging.getLogger(self.__class__.__name__)
        if not COINMARKETCAP_API_KEY:
            raise ValueError("API Key for CoinMarketCap is missing from omega_secrets.py.")
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}
        self.session = Session()
        self.session.headers.update(self.headers)

    def get_top_coins_data(self, limit: int = 250) -> List[Dict[str, Any]]:
        """
        Fetches a full list of top coins with all their market data.
        """
        url = f'{self.api_url}/v1/cryptocurrency/listings/latest'
        parameters = {'start': '1', 'limit': str(limit), 'convert': 'USD'}
        try:
            self.logger.info(f"Fetching top {limit} coins from CoinMarketCap...")
            response = self.session.get(url, params=parameters, timeout=20)
            response.raise_for_status()
            json_response = response.json()
            data = json_response.get('data')
            if not data:
                raise CMCAPIError("CMC API returned no data in 'data' field.")
            
            processed_data = []
            for coin in data:
                quote = coin.get('quote', {}).get('USD', {})
                processed_data.append({
                    'id': coin.get('id'),
                    'name': coin.get('name'),
                    'symbol': coin.get('symbol'),
                    'price_usd': float(quote.get('price', 0.0) or 0.0),
                    'market_cap_usd': float(quote.get('market_cap', 0.0) or 0.0),
                    'total_volume_usd': float(quote.get('volume_24h', 0.0) or 0.0),
                    'percent_change_24h': float(quote.get('percent_change_24h', 0.0) or 0.0),
                })
            return processed_data
        except exceptions.RequestException as e:
            self.logger.critical(f"Critical error fetching top coins from CoinMarketCap: {e}")
            raise CMCAPIError(e)
        except (ValueError, KeyError) as e:
            self.logger.critical(f"Critical error processing CMC data: {e}")
            raise CMCAPIError(e)
