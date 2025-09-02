# data_sources.py (v6.1 - The Architect's Promise)

import requests
import logging
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    from config import API_KEYS, MARKET_PARAMETERS
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"FATAL: आवश्यक पुस्तकालय हराएको छ: {e}")
    print("कृपया 'pip install beautifulsoup4 lxml' चलाउनुहोस्।")
    nltk.download('vader_lexicon'); exit()

thread_local = threading.local()

def get_thread_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
        thread_local.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    return thread_local.session

class OracleEngine:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.cmc_api_key = API_KEYS.get("market_data", {}).get("coinmarketcap")
        
        self.tier1_key = API_KEYS.get("news_tier1_aggregators", {}).get('cryptopanic')
        self.tier1_url = "https://cryptopanic.com/api/v1/posts/"
        
        tier2_available = [item for item in API_KEYS.get("news_tier2_general", {}).items() if item[1]]
        self.tier2_apis = deque(tier2_available)
        self.api_lock = threading.Lock()
        
        self.logger.info(f"Triumvirate Engine (v6.1) प्रारम्भ भयो। {len(self.tier2_apis)} शाही रक्षकहरू र सम्राटको आँखा तयार छन्।")

    def _fetch(self, url, params=None, headers=None):
        session = get_thread_session()
        try:
            response = session.get(url, params=params, headers=headers, timeout=20)
            response.raise_for_status()
            return response # <-- बन्द बाकस (Response object) फर्काउने
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"API अनुरोध असफल: {url.split('/')[2]} - {e}")
        return None

    def _fetch_news_tier1(self, symbol):
        params = {"auth_token": self.tier1_key, "currencies": symbol, "public": "true"}
        response = self._fetch(self.tier1_url, params=params)
        if response:
            data = response.json() # <-- समाधान: बाकसलाई यहाँ खोल्ने
            return [post['title'] for post in data.get('results', [])]
        return None

    def _fetch_news_tier2(self, symbol):
        with self.api_lock:
            if not self.tier2_apis: return None
            api_name, api_key = self.tier2_apis[0]; self.tier2_apis.rotate(-1)
        
        self.logger.info(f"'{symbol}' को लागि शाही रक्षक '{api_name}' तैनाथ गर्दै...")
        if api_name == 'gnews_io':
            url = f"https://gnews.io/api/v4/search?q={symbol}&token={api_key}&lang=en&topic=crypto"
            response = self._fetch(url)
            if response:
                return [a['title'] for a in response.json().get('articles', [])] # <-- समाधान: बाकसलाई यहाँ खोल्ने
        return None

    def _fetch_news_tier3_google(self, coin_name):
        self.logger.info(f"'{coin_name}' को लागि सम्राटको आँखा (Google News) प्रयोग गर्दै...")
        try:
            url = f"https://news.google.com/rss/search?q={coin_name}+crypto&hl=en-US&gl=US&ceid=US:en"
            response = self._fetch(url)
            if response:
                # Google News को लागि हामीलाई बाकस नै चाहिन्छ, त्यसैले यहाँ .json() प्रयोग नगर्ने
                soup = BeautifulSoup(response.text, 'xml')
                return [item.title.text for item in soup.findAll('item')[:10]]
        except Exception as e:
            self.logger.error(f"Google News स्क्र्यापिङमा त्रुटि: {e}")
        return []

    def get_news_for_coin(self, coin):
        # ... (यो प्रकार्यमा कुनै परिवर्तन छैन)
        symbol = coin.get('symbol', ''); name = coin.get('name', '')
        news = self._fetch_news_tier1(symbol)
        if news is not None: return news
        self.logger.warning(f"'{symbol}' को लागि Tier 1 असफल। Tier 2 मा जाँदै...")
        news = self._fetch_news_tier2(symbol)
        if news is not None: return news
        self.logger.warning(f"'{symbol}' को लागि Tier 2 असफल। Tier 3 (सम्राटको आँखा) तैनाथ गर्दै...")
        return self._fetch_news_tier3_google(name)

    def _synthesize_single_coin(self, coin):
        # ... (यो प्रकार्यमा कुनै परिवर्तन छैन)
        news_titles = self.get_news_for_coin(coin)
        sentiment_score = 0.0
        if news_titles:
            compound_scores = [self.sentiment_analyzer.polarity_scores(title)['compound'] for title in news_titles]
            sentiment_score = sum(compound_scores) / len(compound_scores)
        quote = coin.get('quote', {}).get('USD', {}); market_cap = quote.get('market_cap', 1); volume = quote.get('volume_24h', 0)
        base = 50; sentiment = sentiment_score * 30; news_count = min(len(news_titles), 20); liquidity = min((volume / market_cap) * 20, 10)
        conviction = max(0, min(100, base + sentiment + news_count + liquidity))
        return {'symbol': coin['symbol'], 'name': coin['name'], 'price': quote.get('price', 0), 'market_cap': market_cap, 'volume_24h': volume, 'sentiment_score': sentiment_score, 'news_article_count': len(news_titles), 'conviction_score': conviction}

    def scan_and_synthesize(self):
        headers = {'X-CMC_PRO_API_KEY': self.cmc_api_key}
        response = self._fetch('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', params={'limit': '5000'}, headers=headers)
        
        # --- समाधान: मुख्य CoinMarketCap को बाकसलाई यहाँ खोल्ने ---
        data = response.json() if response else None
        
        all_coins = data.get('data', []) if data else []
        eligible_coins = [c for c in all_coins if (c.get('quote',{}).get('USD',{}).get('price',1e9) < MARKET_PARAMETERS['max_coin_price'] and c.get('quote',{}).get('USD',{}).get('volume_24h',0) > MARKET_PARAMETERS['min_volume_24h'] and c.get('quote',{}).get('USD',{}).get('market_cap',0) > MARKET_PARAMETERS['min_market_cap'])]
        
        self.logger.info(f"ब्रह्माण्ड स्क्यान सम्पन्न। {len(eligible_coins)} सिक्काहरूले 'सुनौलो फिल्टर' पास गरे।")
        if not eligible_coins: return [], {}

        self.logger.info(f"ट्राइअमभाइरेट इन्जिन तैनाथ गर्दै: {len(eligible_coins)} लक्ष्यहरूको लागि समानान्तर विश्लेषण।")
        final_candidates = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._synthesize_single_coin, coin) for coin in eligible_coins]
            for future in as_completed(futures):
                try: final_candidates.append(future.result())
                except Exception as exc: self.logger.error(f"सिक्का संश्लेषणमा त्रुटि: {exc}")

        final_candidates.sort(key=lambda x: x['conviction_score'], reverse=True)
        market_pulse = {'best_rejected': f"{final_candidates[0]['name']} ({final_candidates[0]['conviction_score']:.1f}%)" if final_candidates else "N/A"}
        return final_candidates, market_pulse

def run_oracle_engine():
    engine = OracleEngine()
    return engine.scan_and_synthesize()
