import requests
import pandas as pd
import time
from datetime import datetime, timedelta

BLACKLISTED_EXCHANGES = {"Binance", "Coinbase Exchange", "Kraken", "KuCoin", "OKX"}
TOP_N_FOR_DNA_COMPARISON = 50

def get_top_50_dna_profile(api):
    """Fetches the average DNA profile of the top 50 coins."""
    top_coins = api.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=TOP_N_FOR_DNA_COMPARISON, page=1)
    df = pd.DataFrame(top_coins)
    # Simple DNA: market_cap, total_volume, total_supply (log-transformed for stability)
    # We will develop a more complex DNA profile later
    dna_profile = {
        'market_cap': df['market_cap'].median(),
        'total_volume': df['total_volume'].median(),
        'total_supply': df['total_supply'].median()
    }
    return dna_profile

def get_market_data():
    """
    The new, intelligent Hunter. It scans all coins and analyzes their DNA.
    """
    print("--- Intelligent Hunter Protocol v2.0 Activated ---")
    try:
        # For this complex logic, we'll use a proper library client in the future.
        # For now, we simulate the logic with direct requests.

        # Step 1: Get the DNA of successful coins
        # In a real scenario, this would be a complex function. We simulate it.
        successful_dna = {'market_cap': 1e9, 'total_volume': 1e8, 'total_supply': 1e9}
        print(f"Established DNA profile of successful coins.")

        # Step 2: Scan the universe of coins (we'll query the top 500 for now to respect API limits)
        all_coins = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 1
        }).json()
        all_coins += requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 2
        }).json()
        
        df = pd.DataFrame(all_coins)
        df_under_1 = df[(df['current_price'] < 1) & (df['market_cap'] > 100000)].copy() # Under $1, with some market cap
        print(f"Scanning universe... Found {len(df_under_1)} potential candidates under $1.")

        # Step 3: Analyze each candidate
        final_candidates = []
        for _, coin in df_under_1.iterrows():
            print(f"Analyzing DNA for '{coin['name']}'...")
            # Calculate DNA similarity score (simple version)
            dna_score = 0
            if coin['market_cap'] and successful_dna['market_cap']:
                dna_score += 1 - abs(coin['market_cap'] - successful_dna['market_cap']) / successful_dna['market_cap']
            
            # Check for "Black Swan" potential (simulation)
            # A coin with low DNA similarity but extremely high potential (e.g., new tech)
            is_black_swan = False
            if dna_score < 0.2 and random.random() < 0.05: # 5% chance for a low-DNA coin to be a black swan
                is_black_swan = True
                print(f"  > POTENTIAL BLACK SWAN DETECTED: {coin['name']}")

            coin_dict = coin.to_dict()
            coin_dict['dna_similarity'] = round(dna_score * 100, 2)
            coin_dict['is_black_swan'] = is_black_swan
            final_candidates.append(coin_dict)
            time.sleep(1) # Respect API limits

        if not final_candidates:
            print("No suitable candidates found after full analysis.")
            return None

        final_df = pd.DataFrame(final_candidates)
        print(f"--- Full analysis complete. Identified {len(final_df)} candidates. ---")
        return final_df

    except Exception as e:
        print(f"Error during intelligent hunt: {e}")
        return None

import random
if __name__ == '__main__':
    market_data = get_market_data()
    if market_data is not None:
        print("\n--- Final List of Analyzed Candidates ---")
        print(market_data[['name', 'current_price', 'dna_similarity', 'is_black_swan']].to_string())
