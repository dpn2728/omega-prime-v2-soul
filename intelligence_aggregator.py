# intelligence_aggregator.py (v1.5 - The Batch Commander)
import requests, logging
from config import API_KEYS
# ... (imports and class definition are the same)
class IntelligenceAggregator:
    # ... (__init__ and get_sentiment_score are the same)
    def aggregate_intelligence_in_batch(self, symbols_list):
        if not self.api_key: return {}
        logger.info(f"{len(symbols_list)} सिक्काहरूको लागि ब्याचमा गुप्तचर सङ्कलन गर्दै...")
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {"auth_token": self.api_key, "currencies": ",".join(symbols_list), "public": "true"}
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            news_by_symbol = {symbol: [] for symbol in symbols_list}
            if data and 'results' in data:
                for post in data['results']:
                    if 'title' in post and 'currencies' in post:
                        for currency in post['currencies']:
                            if currency['code'] in news_by_symbol:
                                news_by_symbol[currency['code']].append(post['title'])
            
            sentiment_by_symbol = {symbol: self.get_sentiment_score(titles) for symbol, titles in news_by_symbol.items()}
            return sentiment_by_symbol
        except Exception as e:
            logger.error(f"CryptoPanic ब्याच अनुरोधमा त्रुटि: {e}")
            return {}
# Full code for clarity
import requests, logging
from config import API_KEYS
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except ImportError:
    nltk.download('vader_lexicon'); from nltk.sentiment.vader import SentimentIntensityAnalyzer
logger = logging.getLogger(__name__)
class IntelligenceAggregator:
    def __init__(self):
        self.session = requests.Session(); self.session.headers.update({'User-Agent': 'OmegaPrime/1000.0'}); self.sentiment_analyzer = SentimentIntensityAnalyzer(); self.api_key = API_KEYS.get("tier1_intelligence", {}).get("cryptopanic")
    def get_sentiment_score(self, texts):
        if not texts: return 0.0; scores = [self.sentiment_analyzer.polarity_scores(text)['compound'] for text in texts]; return sum(scores) / len(scores)
    def aggregate_intelligence_in_batch(self, symbols_list):
        if not self.api_key or not symbols_list: return {}
        logger.info(f"{len(symbols_list)} सिक्काहरूको लागि ब्याचमा गुप्तचर सङ्कलन गर्दै...")
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {"auth_token": self.api_key, "currencies": ",".join(symbols_list), "public": "true"}
        try:
            response = self.session.get(url, params=params, timeout=30); response.raise_for_status(); data = response.json()
            news_by_symbol = {symbol: [] for symbol in symbols_list}
            if data and 'results' in data:
                for post in data['results']:
                    if 'title' in post and 'currencies' in post:
                        for currency in post['currencies']:
                            symbol = currency['code'].upper()
                            if symbol in news_by_symbol: news_by_symbol[symbol].append(post['title'])
            sentiment_by_symbol = {symbol: self.get_sentiment_score(titles) for symbol, titles in news_by_symbol.items()}
            logger.info("ब्याच गुप्तचर सङ्कलन सम्पन्न।")
            return sentiment_by_symbol
        except Exception as e:
            logger.error(f"CryptoPanic ब्याच अनुरोधमा त्रुटि: {e}"); return {}
