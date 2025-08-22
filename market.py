import requests
import pandas as pd

def get_market_data():
    """
    Fetches market data for the top 250 cryptocurrencies from CoinGecko.
    Filters for coins under $2 as per 'The Hunt' protocol.
    """
    print("Fetching market data from CoinGecko...")
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        # Convert to a Pandas DataFrame for easier manipulation
        df = pd.DataFrame(data)

        # --- THE HUNT PROTOCOL: PRICE CONSTRAINT ---
        # Keep only the coins that are under $2
        filtered_df = df[df['current_price'] < 2].copy()
        print(f"Successfully fetched data for {len(data)} coins.")
        print(f"Found {len(filtered_df)} coins under $2.")

        return filtered_df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return None

if __name__ == '__main__':
    # This allows you to test the file directly
    market_data = get_market_data()
    if market_data is not None:
        print("\nSample of fetched data:")
        print(market_data.head())
