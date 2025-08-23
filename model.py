import pandas as pd

def generate_directive(market_data):
    """
    यो ओमेगा प्राइमको मस्तिष्कको पहिलो संस्करण हो।
    यसले बजारको डाटा लिन्छ र "Genesis" वा "Hold" आदेश जारी गर्ने निर्णय गर्छ।
    """
    # यदि कुनै डाटा आएन भने, सुरक्षित रहन 'Hold' गर्ने।
    if not isinstance(market_data, list) or not market_data:
        print("MIND: No market data received. Defaulting to HOLD.")
        return create_hold_directive("No valid market data received.")

    # डाटालाई Pandas DataFrame मा रूपान्तरण गर्ने, जसले विश्लेषणलाई सजिलो बनाउँछ।
    df = pd.DataFrame(market_data)

    # --- हाम्रो पहिलो, सरल "Genesis" को नियम ---
    # नियम: यदि कुनै कोइनको मूल्य पछिल्लो २४ घण्टामा १०% भन्दा बढी र ३०% भन्दा कमले बढेको छ भने,
    # त्यो हाम्रो लागि एक सम्भावित "Genesis" उम्मेदवार हो।
    
    # 'price_change_percentage_24h' स्तम्भ अवस्थित छ कि छैन भनी जाँच्ने
    if 'price_change_percentage_24h' not in df.columns:
        print("MIND: 'price_change_percentage_24h' column not found. Defaulting to HOLD.")
        return create_hold_directive("Market data is missing the required 'price_change_percentage_24h' field.")

    # None/NaN मानहरूलाई 0 ले भर्ने
    df['price_change_percentage_24h'] = df['price_change_percentage_24h'].fillna(0)

    # हाम्रो नियमअनुसार सम्भावित उम्मेदवारहरू फिल्टर गर्ने
    potential_candidates = df[
        (df['price_change_percentage_24h'] > 10) & 
        (df['price_change_percentage_24h'] < 30)
    ]

    # --- निर्णय लिने ---
    if not potential_candidates.empty:
        # यदि उम्मेदवारहरू भेटिए भने, सबैभन्दा बढी मूल्य परिवर्तन भएकोलाई छान्ने
        best_candidate = potential_candidates.sort_values(by='price_change_percentage_24h', ascending=False).iloc[0]
        print(f"MIND: Genesis candidate found! Coin: {best_candidate['name']}")
        return create_genesis_directive(best_candidate)
    else:
        # यदि कुनै उम्मेदवार भेटिएन भने, 'Hold' गर्ने
        print("MIND: No suitable Genesis candidate found. Issuing HOLD directive.")
        return create_hold_directive("No coins met the 10%-30% price change criteria.")

def create_genesis_directive(coin_data):
    """
    एक 'Genesis' आदेशको लागि डाटा संरचना (structure) बनाउँछ।
    """
    directive = {
        "type": "GENESIS",
        "coin_name": coin_data.get('name', 'N/A'),
        "coin_symbol": coin_data.get('symbol', 'N/A').upper(),
        "current_price": coin_data.get('current_price', 0),
        "price_change_24h": coin_data.get('price_change_percentage_24h', 0),
        "reason": f"Detected a significant but not overly-hyped 24-hour price increase of {coin_data.get('price_change_percentage_24h', 0):.2f}%."
    }
    return directive

def create_hold_directive(reason):
    """
    एक 'Hold' आदेशको लागि डाटा संरचना बनाउँछ।
    """
    directive = {
        "type": "HOLD",
        "reason": reason
    }
    return directive
