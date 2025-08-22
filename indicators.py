import pandas_ta as ta

def apply_technical_indicators(df):
    """
    Applies a set of technical indicators to the market data DataFrame.
    This forms a part of the coin's "DNA" analysis.
    """
    if df is None or df.empty:
        print("Cannot apply indicators: DataFrame is empty.")
        return None

    print("Applying technical indicators (RSI, SMA)...")
    try:
        # --- The Analysis Protocol ---
        # Calculate RSI (Relative Strength Index) over a 14-day period
        df.ta.rsi(length=14, append=True)

        # Calculate 50-day and 200-day Simple Moving Averages (SMA)
        df.ta.sma(length=50, append=True)
        df.ta.sma(length=200, append=True)

        # Clean up the column names for better readability
        df.rename(columns={'RSI_14': 'RSI', 'SMA_50': 'SMA50', 'SMA_200': 'SMA200'}, inplace=True)

        print("Successfully applied technical indicators.")
        return df

    except Exception as e:
        print(f"Error applying technical indicators: {e}")
        return None

if __name__ == '__main__':
    # This part is for testing the file directly
    # We need a sample DataFrame similar to what market.py provides
    import pandas as pd
    sample_data = {'high': [10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                   'low': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                   'close': [9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}
    sample_df = pd.DataFrame(sample_data)

    # To calculate RSI, we need the 'close' price column
    # pandas-ta is smart enough to find it.
    analyzed_df = apply_technical_indicators(sample_df)
    if analyzed_df is not None:
        print("\nSample of analyzed data:")
        print(analyzed_df)
