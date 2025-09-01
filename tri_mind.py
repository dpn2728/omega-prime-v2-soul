# tri_mind.py (v3.0 - The Evolved Living Brain of the Empire)

import logging
import numpy as np
from scipy.stats import linregress
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

class BaseMind:
    """सबै विशेषज्ञ मस्तिष्कहरूको लागि आधार वर्ग।"""
    def __init__(self, mind_name):
        self.mind_name = mind_name
        self.logger = logging.getLogger(f"TriMind.{self.mind_name}")

    def analyze(self, coin_data, market_condition='neutral'):
        raise NotImplementedError("प्रत्येक मस्तिष्कले 'analyze' विधि लागू गर्नुपर्छ।")

# --- विशेषज्ञ मस्तिष्क #1: The Prophet (The Oracle Mind) v3.0 ---
class ProphetMind(BaseMind):
    """ऐतिहासिक प्रवृत्ति, समाचारको गहिराइ, र बजार क्यापको आधारमा विश्लेषण गर्दछ।"""
    def __init__(self):
        super().__init__("Prophet")

    def _calculate_trend_slope(self, historical_prices):
        """ऐतिहासिक मूल्यहरूको प्रवृत्ति ढलान (trend slope) गणना गर्दछ।"""
        if not historical_prices or len(historical_prices) < 7: return 0
        y = np.array(historical_prices)
        x = np.arange(len(y))
        slope, _, _, _, _ = linregress(x, y)
        return slope

    def analyze(self, coin_data, market_condition='neutral'):
        self.logger.debug(f"'{coin_data['symbol']}' को वृद्धि सम्भावनाको विश्लेषण गर्दै...")
        score = 0
        reasons = []

        # विश्लेषण १: ऐतिहासिक मूल्य प्रवृत्ति (Historical Trend)
        trend_slope = self._calculate_trend_slope(coin_data.get('historical_prices', []))
        if trend_slope > 0.5: # अझ कडा मापदण्ड
            score += 25
            reasons.append(f"Strong positive 30d price trend (slope: {trend_slope:.4f})")
        
        # विश्लेषण २: बजार क्याप "Sweet Spot"
        mc = coin_data.get('market_cap', 0)
        if 100000 < mc <= 1000000: score += 30; reasons.append("Micro-cap with high potential")
        elif 1000000 < mc <= 5000000: score += 15
        
        # विश्लेषण ३: समाचारको गहिराइ (News Depth & Sentiment - v3.0 upgrade)
        sentiment = coin_data.get('sentiment_score', 0)
        article_count = coin_data.get('news_article_count', 0)
        if sentiment > 0.5 and article_count > 5:
            score += 35
            reasons.append(f"CRITICAL: Strong, widespread positive sentiment ({sentiment:.2f} from {article_count} articles)")
        elif sentiment > 0.2:
            score += 10
            reasons.append(f"Moderate positive sentiment ({sentiment:.2f})")
        
        confidence = max(0, min(100, int(score)))
        threshold = get_adaptive_thresholds(market_condition)['prophet']
        verdict = confidence >= threshold
        
        return verdict, confidence, reasons

# --- विशेषज्ञ मस्तिष्क #2: The Strategist (The Risk/Reward Mind) v3.0 ---
class StrategistMind(BaseMind):
    """अस्थिरता, तरलता, र बजारको अवस्थाको आधारमा जोखिम विश्लेषण गर्दछ।"""
    def __init__(self):
        super().__init__("Strategist")

    def _calculate_volatility(self, historical_prices):
        if not historical_prices or len(historical_prices) < 2: return 0.0
        prices = np.array(historical_prices)
        log_returns = np.log(prices[1:] / prices[:-1])
        daily_std = np.std(log_returns)
        return daily_std * np.sqrt(365) # Annualize

    def analyze(self, coin_data, market_condition='neutral'):
        self.logger.debug(f"'{coin_data['symbol']}' को लागि जोखिम/पुरस्कार विश्लेषण गर्दै...")
        risk_score = 0
        reasons = []

        # विश्लेषण १: अस्थिरता (Volatility)
        volatility = self._calculate_volatility(coin_data.get('historical_prices', []))
        if volatility > 2.5: risk_score += 40; reasons.append(f"Extreme volatility ({volatility:.2f})")
        elif volatility > 1.5: risk_score += 20; reasons.append(f"High volatility ({volatility:.2f})")

        # विश्लेषण २: तरलता (Liquidity - Volume/MC ratio)
        mc = coin_data.get('market_cap', 1)
        vol = coin_data.get('volume', 0)
        liquidity_ratio = (vol / mc) * 100 if mc > 0 else 0
        if liquidity_ratio < 10: # अझ कडा मापदण्ड
            risk_score += 50; reasons.append(f"CRITICAL: Low liquidity ({liquidity_ratio:.2f}%)")
        
        confidence = max(0, 100 - int(risk_score))
        threshold = get_adaptive_thresholds(market_condition)['strategist']
        verdict = confidence >= threshold
        
        return verdict, confidence, reasons

# --- विशेषज्ञ मस्तिष्क #3: The Guardian (The Security Mind) v3.0 ---
class GuardianMind(BaseMind):
    """अन-चेन सुरक्षा 'रेड फ्ल्यागहरू' को विश्लेषण गर्दछ र VETO शक्ति प्रयोग गर्दछ।"""
    def __init__(self):
        super().__init__("Guardian")

    def analyze(self, coin_data, market_condition='neutral'):
        self.logger.debug(f"'{coin_data['symbol']}' को लागि सुरक्षा विश्लेषण गर्दै...")
        red_flags = 0
        reasons = []
        security_info = coin_data.get('on_chain_security', {})

        # विश्लेषण १: स्मार्ट कन्ट्र्याक्ट प्रमाणीकरण (v3.0 VETO Power)
        is_verified = security_info.get('source_code_verified', False)
        if not is_verified and coin_data.get('contract_address'): # Check only if it's a token
            red_flags = 10 # Max red flags
            reasons.append("FATAL VETO: Smart contract source code is NOT verified.")
        else:
            reasons.append("Contract source code verified.")
        
        # भविष्यका अन्य सुरक्षा जाँचहरू यहाँ थप्न सकिन्छ...

        confidence = max(0, 100 - (red_flags * 25))
        threshold = get_adaptive_thresholds(market_condition)['guardian']
        verdict = confidence >= threshold
        
        return verdict, confidence, reasons

# --- गतिशील थ्रेसहोल्ड इन्जिन ---
def get_adaptive_thresholds(market_condition='neutral'):
    """बजारको अवस्था अनुसार स्वीकृति थ्रेसहोल्डहरू समायोजन गर्दछ।"""
    if market_condition == 'bullish': # Riskier bets are more acceptable
        return {'prophet': 60, 'strategist': 40, 'guardian': 50}
    if market_condition == 'bearish': # Only the absolute best candidates
        return {'prophet': 80, 'strategist': 60, 'guardian': 75}
    # Neutral/Default
    return {'prophet': 70, 'strategist': 50, 'guardian': 70}

# --- मुख्य अर्केस्ट्रेटर (The Main Orchestrator) ---
def analyze_single_coin_for_batch(coin_data, market_condition='neutral'):
    prophet = ProphetMind()
    strategist = StrategistMind()
    guardian = GuardianMind()

    prophet_verdict, prophet_conf, prophet_reasons = prophet.analyze(coin_data, market_condition)
    strategist_verdict, strategist_conf, strategist_reasons = strategist.analyze(coin_data, market_condition)
    guardian_verdict, guardian_conf, guardian_reasons = guardian.analyze(coin_data, market_condition)
    
    final_verdict = all([prophet_verdict, strategist_verdict, guardian_verdict])
    
    return {
        'symbol': coin_data['symbol'], 'name': coin_data['name'],
        'final_verdict': 'APPROVED' if final_verdict else 'REJECTED',
        'prophet_mind': {'verdict': prophet_verdict, 'confidence': prophet_conf, 'reasons': prophet_reasons},
        'strategist_mind': {'verdict': strategist_verdict, 'confidence': strategist_conf, 'reasons': strategist_reasons},
        'guardian_mind': {'verdict': guardian_verdict, 'confidence': guardian_conf, 'reasons': guardian_reasons}
    }

def run_tri_mind_consensus_for_batch(coins_batch, market_condition='neutral'):
    logger = logging.getLogger("TriMind.Orchestrator")
    logger.info(f"👑 जीवित मस्तिष्क (v3.0) ले {len(coins_batch)} सिक्काहरूको ब्याचको विश्लेषण सुरु गर्यो।")
    analysis_results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(analyze_single_coin_for_batch, coin, market_condition) for coin in coins_batch]
        for future in futures:
            try:
                analysis_results.append(future.result())
            except Exception as e:
                logger.error(f"सिक्का विश्लेषणमा त्रुटि: {e}", exc_info=True)

    approved_coins = [r for r in analysis_results if r['final_verdict'] == 'APPROVED']
    logger.info(f"🧠 विश्लेषण सम्पन्न। {len(approved_coins)}/{len(coins_batch)} सिक्काहरू स्वीकृत भए।")
    return approved_coins # अब केवल स्वीकृत सिक्काहरू मात्र फर्काउने

# --- आत्म-परीक्षण ब्लक (v3.0) ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    mock_coins = [
        { # उत्तम उम्मेदवार
            'name': 'GoodCoin', 'symbol': 'GOOD', 'market_cap': 800000, 'volume': 600000,
            'sentiment_score': 0.8, 'news_article_count': 10,
            'historical_prices': np.linspace(100, 180, 30), # Strong trend
            'contract_address': '0x123', 'on_chain_security': {'source_code_verified': True}
        },
        { # Guardian VETO को शिकार
            'name': 'ShadyCoin', 'symbol': 'SHADY', 'market_cap': 1200000, 'volume': 800000,
            'sentiment_score': 0.9, 'news_article_count': 20,
            'historical_prices': np.linspace(100, 200, 30),
            'contract_address': '0x456', 'on_chain_security': {'source_code_verified': False} # The VETO trigger
        },
        { # Prophet द्वारा अस्वीकृत (कम समाचार)
            'name': 'QuietCoin', 'symbol': 'QUIET', 'market_cap': 900000, 'volume': 500000,
            'sentiment_score': 0.7, 'news_article_count': 2, # Fails the Prophet's new check
            'historical_prices': np.linspace(100, 160, 30),
            'contract_address': '0x789', 'on_chain_security': {'source_code_verified': True}
        }
    ]
    
    print("\n--- परीक्षण: जीवित मस्तिष्क v3.0 ---")
    approved_results = run_tri_mind_consensus_for_batch(mock_coins, market_condition='neutral')
    
    print("\n--- स्वीकृत उम्मेदवारहरू ---")
    if approved_results:
        pprint(approved_results)
    else:
        print("कुनै पनि उम्मेदवार स्वीकृत भएन।")
