# model.py (Final Version - Ready for AI Integration)

import numpy as np

def generate_conviction_score(coin_details: dict, config: dict) -> float:
    """
    The Ultimate Quantum Brain v2.0. Analyzes metrics using a dynamic, multi-factor,
    risk-adjusted scoring model.
    """
    score = 0
    
    # --- 1. Safe Data Extraction ---
    change_24h = coin_details.get('percent_change_24h')
    volume_24h = coin_details.get('total_volume_usd')
    market_cap = coin_details.get('market_cap_usd')
    rsi = coin_details.get('rsi')
    sma_fast = coin_details.get('sma_fast')
    sma_slow = coin_details.get('sma_slow')
    
    # --- 2. Pre-condition Penalties (Critical Risk Factors) ---
    if isinstance(change_24h, (int, float)) and change_24h < 0:
        return 0.0 # Hard filter for negative momentum coins

    if rsi is not None and rsi >= 80:
        return 5.0 # Very low score for extreme overbought condition

    # --- 3. Weighted Scoring Modules ---
    
    # Price Momentum
    if isinstance(change_24h, (int, float)):
        if change_24h > 25: score += 30
        elif change_24h > 15: score += 20
        elif change_24h > 10: score += 10

    # Volume Velocity
    if isinstance(volume_24h, (int, float)) and isinstance(market_cap, (int, float)) and market_cap > 1000000:
        volume_mc_ratio = (volume_24h / market_cap) * 100
        if volume_mc_ratio > 100: score += 25
        elif volume_mc_ratio > 50: score += 15

    # Trend Consistency & Strength (SMA Crossover)
    if isinstance(sma_fast, (int, float)) and isinstance(sma_slow, (int, float)) and sma_fast > sma_slow:
        crossover_strength = ((sma_fast - sma_slow) / sma_slow) * 100
        if crossover_strength > 5: score += 20
        elif crossover_strength > 1: score += 10
    
    # RSI Condition
    if rsi is not None:
        if 60 <= rsi < 70: score += 15
        elif rsi >= 70: score -= 10

    # Market Cap Bonus
    if isinstance(market_cap, (int, float)) and market_cap > 1_000_000_000:
        score += 5
        
    # --- 4. Final Score Clamping ---
    final_score = np.clip(score, 0, 100)
    
    return float(final_score)

def get_predictive_analysis(coin_details: dict) -> float:
    """
    Placeholder for future, true AI/ML predictive models.
    This function will be replaced with a neural network or similar model
    that analyzes historical data to predict future price movements.
    
    For now, it returns a neutral, non-influential score.
    """
    return 50.0
