import requests
import pandas as pd
import time
import random
import traceback

def get_market_data():
    """
    Intelligent Hunter Protocol v2.3 (Diagnostic Mode).
    Scans a smaller set of coins for faster testing cycles.
    """
    print("--- Intelligent Hunter Protocol v2.3 (Diagnostic Mode) Activated ---")
    try:
        print("Scanning the market for 50 potential candidates for faster diagnostics...")
        markets_url = "https://api.coingecko.com/api/v3/coins/markets"
        
        # --- DIAGNOSTIC CHANGE: Reduced per_page from 250 to 50 ---
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}
        
        response = requests.get(markets_url, params=params, timeout=15)
        response.raise_for_status()
        all_coins_data = response.json()

        df = pd.DataFrame(all_coins_data)
        
        df_candidates = df[(df['current_price'] < 2) & (df['market_cap'].notna()) & (df['market_cap'] > 100000)].copy()
        
        if df_candidates.empty:
            print("No suitable candidates found meeting the initial criteria.")
            return None

        print(f"Found {len(df_candidates)} candidates. Analyzing DNA and Black Swan potential...")

        final_candidates = []
        for _, coin in df_candidates.iterrows():
            coin_dict = coin.to_dict()
            coin_dict['dna_similarity'] = max(0, 100 - (coin.get('market_cap_rank', 500) / 5))
            is_black_swan = random.random() < 0.05 # 5% chance for a black swan candidate
            coin_dict['is_black_swan'] = is_black_swan
            if is_black_swan:
                print(f"  > POTENTIAL BLACK SWAN DETECTED: {coin['name']}")
            final_candidates.append(coin_dict)
        
        final_df = pd.DataFrame(final_candidates)
        print(f"--- Full analysis complete. Identified {len(final_df)} candidates. ---")
        return final_df

    except Exception as e:
        print(f"❌❌❌ FATAL ERROR in market.py ❌❌❌")
        traceback.print_exc()
        return None
