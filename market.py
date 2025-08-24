import requests

def get_market_data():
    """
    यो ओमेगा प्राइमको आँखा हो। यसले CoinGecko बाट बजारको डाटा तान्छ।
    """
    print("SENSE: Awakening the eye of the hunter (CoinGecko)...")
    
    # हामी CoinGecko API बाट शीर्ष १०० कोइनहरूको बजार डाटा तान्छौं
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100, # शीर्ष १०० कोइनहरू
        "page": 1,
        "sparkline": "false"
    }
    
    try:
        # १० सेकेन्डको टाइमआउटको साथ अनुरोध पठाउने
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # 4xx or 5xx त्रुटिहरूको लागि जाँच गर्छ
        print("SENSE: Market data successfully captured.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"🔥 SENSE ERROR: Failed to capture market data. The eye is blind. Error: {e}")
        return [] # त्रुटि भएमा खाली सूची फर्काउने, ताकि प्रणाली क्र्यास नहोस्
