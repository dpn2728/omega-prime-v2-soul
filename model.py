import pandas as pd

def generate_directive(market_data):
    """
    यो ओमेगा प्राइमको शिकारी मस्तिष्क हो।
    यसले बजार डाटाको विश्लेषण गरेर 'Genesis' वा 'Hold' को निर्णय लिन्छ।
    """
    print("MIND: The hunter's brain is analyzing the captured data...")
    
    # यदि आँखाले केही देखेन भने (डाटा खाली छ), सुरक्षित रहन 'Hold' गर्ने
    if not market_data:
        print("MIND: Analysis complete. The data is empty. Directive is HOLD.")
        return {"type": "HOLD", "reason": "Failed to capture any market data from the Senses."}
    
    # विश्लेषणको लागि डाटालाई Pandas DataFrame मा रूपान्तरण गर्ने
    df = pd.DataFrame(market_data)
    
    # 'price_change_percentage_24h' स्तम्भमा कुनै खाली मान भए, त्यसलाई ० ले भर्ने
    df['price_change_percentage_24h'] = df['price_change_percentage_24h'].fillna(0)
    
    # --- शिकारको नियम ---
    # नियम: १०% भन्दा बढी तर ३०% भन्दा कमले बढेको कोइन खोज्ने
    candidates = df[
        (df['price_change_percentage_24h'] > 10) & 
        (df['price_change_percentage_24h'] < 30)
    ]
    
    # --- निर्णय ---
    if not candidates.empty:
        # यदि उम्मेदवार भेटियो भने, सबैभन्दा बढी बढेकोलाई छान्ने
        best_candidate = candidates.sort_values(by='price_change_percentage_24h', ascending=False).iloc[0]
        candidate_name = best_candidate['name']
        change_percent = best_candidate['price_change_percentage_24h']
        
        print(f"MIND: Analysis complete. GENESIS candidate found: {candidate_name}")
        return {
            "type": "GENESIS",
            "coin_name": candidate_name,
            "reason": f"Price increased by a promising {change_percent:.2f}% in the last 24 hours."
        }
    else:
        # यदि कुनै उम्मेदवार भेटिएन भने, 'Hold' गर्ने
        print("MIND: Analysis complete. No suitable candidate found. Directive is HOLD.")
        return {"type": "HOLD", "reason": "No coins met the Genesis criteria (10% < change < 30%)."}
