import pandas as pd
import random
from datetime import datetime

def predict_with_quantum_brain(analyzed_df):
    """
    रणनीतिकार मस्तिष्क (Strategist Brain) v2.1.
    यसले DNA विश्लेषण र अन्य कारकहरूको आधारमा कुन शाही आदेश जारी गर्ने भनेर निर्णय गर्दछ।
    """
    # यदि कुनै विश्लेषण गर्न योग्य डाटा छैन भने, 'HOLD' आदेश जारी गर्ने।
    if analyzed_df is None or analyzed_df.empty:
        return {"directive_type": "HOLD", "reason": "विश्लेषणको लागि कुनै योग्य बजार डाटा प्राप्त भएन।"}

    print("क्वान्टम ब्रेन (रणनीतिकार v2.1) ले DNA प्रोफाइलहरूको विश्लेषण गर्दैछ...")

    # --- उद्देश्य #29: "भविष्यवक्ता" मस्तिष्क ---
    # पहिलो प्राथमिकता: 'ब्ल्याक स्वान' उम्मेदवारहरू खोज्ने।
    # is_black_swan == True भएको डाटा फिल्टर गर्ने।
    black_swan_candidates = analyzed_df[analyzed_df['is_black_swan'] == True]
    if not black_swan_candidates.empty:
        # यदि एक वा बढी 'ब्ल्याक स्वान' भेटिएमा, पहिलोलाई लिने।
        candidate = black_swan_candidates.iloc[0].to_dict()
        print(f"!!! ब्ल्याक स्वान असामान्यता फेला पर्यो: {candidate['name']} !!!")
        return {
            "directive_type": "BLACK_SWAN",
            "coin_data": candidate,
            "summary": "चेतावनी: यो एक उच्च-जोखिम, उच्च-प्रतिफलको सङ्केत हो। यसको DNA, हाम्रो ऐतिहासिक डाटासँग मेल खाँदैन।",
            "thesis": "A calculated gamble on a potential paradigm shift. Max Allocation: 0.5% of portfolio."
        }

    # --- उद्देश्य #11: "जेनेसिस हन्ट" ---
    # दोस्रो प्राथमिकता: राम्रो DNA भएको 'जेनेसिस' उम्मेदवार खोज्ने।
    # DNA समानता ५०% भन्दा बढी भएको डाटा फिल्टर गर्ने।
    genesis_candidates = analyzed_df[analyzed_df['dna_similarity'] > 50]
    if not genesis_candidates.empty:
        # यदि 'जेनेसिस' उम्मेदवारहरू भेटिएमा, सबैभन्दा राम्रो DNA भएकोलाई लिने।
        candidate = genesis_candidates.sort_values(by='dna_similarity', ascending=False).iloc[0].to_dict()
        print(f"!!! उच्च-सम्भावित जेनेसिस उम्मेदवार फेला पर्यो: {candidate['name']} !!!")
        return {
            "directive_type": "GENESIS",
            "coin_data": candidate,
            "conviction_score": candidate['dna_similarity'],
            "summary": f"यसको DNA प्रोफाइल शीर्ष ५० कोइनहरूसँग {candidate['dna_similarity']:.2f}% मिल्दोजुल्दो छ, जसले उच्च सफलताको सम्भावना देखाउँछ।",
            # (alerts.py ले बाँकी जेनेसिस डाटा आफै बनाउनेछ)
        }
    
    # --- उद्देश्य #40: "होल्ड आदेश" ---
    # यदि कुनै विशेष उम्मेदवार भेटिएन भने, 'HOLD' आदेश जारी गर्ने।
    print("कुनै उच्च-विश्वासको अवसर फेला परेन। 'HOLD' आदेश जारी गरिँदैछ।")
    # सबैभन्दा बढी मार्केट क्याप भएकोलाई 'उत्कृष्ट, तर अपर्याप्त' उम्मेदवारको रूपमा देखाउने।
    candidate = analyzed_df.sort_values(by='market_cap', ascending=False).iloc[0].to_dict()
    return {
        "directive_type": "HOLD",
        "coin_data": candidate,
        "reason": "कुनै पनि उम्मेदवारले हाम्रो न्यूनतम DNA समानता थ्रेसहोल्ड पार गरेन। पूँजी संरक्षण आजको उत्तम रणनीति हो।"
    }
