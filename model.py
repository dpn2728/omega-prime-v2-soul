import pandas as pd

def predict_with_quantum_brain(analyzed_df):
    """
    The first iteration of the Quantum Brain.
    Analyzes the data and makes a final call based on a simple logic.
    This will be replaced with a real ML model later.
    """
    if analyzed_df is None or analyzed_df.empty:
        print("Quantum Brain cannot predict: No data provided.")
        return "HOLD", None, "No valid market data."

    print("Quantum Brain is analyzing the opportunities...")

    # --- THE STRATEGIST PROTOCOL (v0.1 - Simple Logic) ---
    # For now, our simple strategy is to find the coin with the highest market cap
    # that is still under $2. This is a placeholder for a real ML prediction.

    # Sort the DataFrame by market cap in descending order
    best_candidate = analyzed_df.sort_values(by='market_cap', ascending=False).iloc[0]

    coin_name = best_candidate['name']
    reason = f"Identified {coin_name} as the highest market cap candidate under $2."
    conviction_score = 75.0 # Placeholder conviction score

    # For now, the brain is cautious and will always advise to HOLD,
    # but it will report what it found.
    final_directive = "HOLD"
    print(f"Quantum Brain decision: {final_directive}. Reason: {reason}")

    return final_directive, best_candidate, reason
