# social.py (Ultimate News & Sentiment Engine v5.0 - Final)
import logging
import asyncio
import httpx
import requests_cache
from typing import Dict, Any, Optional, List, Tuple
from textblob import TextBlob
from tenacity import retry, stop_after_attempt, wait_exponential

from omega_secrets import NEWS_API_KEYS

# --- Setup Caching for all requests ---
# Cache responses for 15 minutes to avoid hitting rate limits on repeated runs
requests_cache.install_cache('omega_prime_cache', backend='sqlite', expire_after=900)

# --- Private API Fetching Functions with Retry Logic ---
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def _fetch_url(client: httpx.AsyncClient, api_name: str, url: str, params: dict = None, headers: dict = None) -> Optional[Dict[str, Any]]:
    try:
        response = await client.get(url, params=params, headers=headers, timeout=20)
        if response.status_code == 429:
            logging.warning(f"{api_name} is rate-limited. Tenacity will retry.")
            raise Exception("Rate limited")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"{api_name} fetch failed on last attempt: {e}")
        raise # Reraise exception to trigger tenacity's next attempt

# --- Main Intelligence Function ---
async def get_news_and_sentiment(asset_name: str, asset_symbol: str) -> Dict[str, Any]:
    logger = logging.getLogger("SocialSense_v5")
    query = f'("{asset_name}" OR "{asset_symbol.upper()}") AND (crypto OR cryptocurrency OR blockchain OR token OR web3)'
    all_headlines = []

    async with httpx.AsyncClient() as client:
        tasks = []
        api_configs = {
            "newsapi_org": ("https://newsapi.org/v2/everything", {'q': query, 'language': 'en'}, "articles", "title"),
            "gnews_io": ("https://gnews.io/api/v4/search", {'q': query, 'lang': 'en'}, "articles", "title"),
            "newsdata_io": ("https://newsdata.io/api/1/news", {'q': query, 'language': 'en'}, "results", "title"),
        }
        for name, (url, params, articles_key, title_key) in api_configs.items():
            if key := NEWS_API_KEYS.get(name):
                params['apiKey' if name == 'newsapi_org' else 'token' if name == 'gnews_io' else 'apikey'] = key
                tasks.append(_fetch_url(client, name, url, params=params))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for res in results:
        if isinstance(res, dict):
            articles = res.get(list(res.keys())[0], []) if isinstance(res, dict) else [] # Heuristic to find article list
            if isinstance(articles, list):
                for article in articles:
                    if isinstance(article, dict) and (title := article.get('title')):
                        all_headlines.append(title)
    
    # --- Advanced NLP & Scoring ---
    if not all_headlines:
        return {"news_volume": 0, "sentiment_polarity": 0.0, "sentiment_subjectivity": 0.0, "sentiment_label": "Neutral"}

    polarity = 0.0
    subjectivity = 0.0
    for title in all_headlines:
        blob = TextBlob(title)
        polarity += blob.sentiment.polarity
        subjectivity += blob.sentiment.subjectivity
    
    avg_polarity = polarity / len(all_headlines)
    avg_subjectivity = subjectivity / len(all_headlines)

    # Convert polarity score to a simple label
    if avg_polarity > 0.15: sentiment_label = "Very Positive"
    elif avg_polarity > 0.05: sentiment_label = "Positive"
    elif avg_polarity < -0.15: sentiment_label = "Very Negative"
    elif avg_polarity < -0.05: sentiment_label = "Negative"
    else: sentiment_label = "Neutral"
        
    logger.info(f"Found {len(all_headlines)} articles for {asset_name}. Avg Polarity: {avg_polarity:.2f}, Avg Subjectivity: {avg_subjectivity:.2f} ({sentiment_label})")

    return {
        "news_volume": len(all_headlines),
        "sentiment_polarity": avg_polarity,
        "sentiment_subjectivity": avg_subjectivity,
        "sentiment_label": sentiment_label
    }
