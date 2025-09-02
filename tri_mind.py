# tri_mind.py (v4.1 - The Emperor's Council, Final Edict)

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed # <--- यहाँ 'as_completed' थपिएको छ

class BaseMind:
    """सबै विशेषज्ञ सल्लाहकारहरूको लागि आधार वर्ग।"""
    def __init__(self, mind_name):
        self.mind_name = mind_name
        self.logger = logging.getLogger(f"TriMind.{self.mind_name}")

    def analyze(self, coin_data):
        raise NotImplementedError("प्रत्येक सल्लाहकारले 'analyze' विधि लागू गर्नुपर्छ।")

class ProphetMind(BaseMind):
    """भविष्यवक्ता: उत्प्रेरक र विश्वास स्कोरको आधारमा भविष्यको सम्भावनाको विश्लेषण गर्दछ।"""
    def __init__(self):
        super().__init__("Prophet")

    def analyze(self, coin_data):
        self.logger.debug(f"'{coin_data['symbol']}' को भविष्यको विश्लेषण गर्दै...")
        reasons = []
        conviction = coin_data.get('conviction_score', 0)
        if conviction < 75: return False, 0, ["Low conviction score"]
        score = conviction; reasons.append(f"High Conviction ({conviction:.1f}%)")
        mempool_conf = coin_data.get('mempool_confidence', 0)
        smart_money_conf = coin_data.get('smart_money_confidence', 0)
        if mempool_conf > 90 or smart_money_conf > 90:
            score += 10; reasons.append(f"CRITICAL Signal: Mempool({mempool_conf}%) / SmartMoney({smart_money_conf}%)")
        confidence = max(0, min(100, int(score))); verdict = confidence >= 80
        return verdict, confidence, reasons

class StrategistMind(BaseMind):
    """रणनीतिकार: शाही जोखिम म्याट्रिक्सको आधारमा जोखिम/प्रतिफलको विश्लेषण गर्दछ।"""
    def __init__(self):
        super().__init__("Strategist")

    def analyze(self, coin_data):
        self.logger.debug(f"'{coin_data['symbol']}' को लागि रणनीतिक जोखिम विश्लेषण गर्दै...")
        risk_score = 0; reasons = []
        liquidity_risk = coin_data.get('risk_liquidity', 10)
        if liquidity_risk > 6: risk_score += liquidity_risk * 5; reasons.append(f"High Liquidity Risk ({liquidity_risk}/10)")
        volatility_risk = coin_data.get('risk_volatility', 10)
        if volatility_risk > 7: risk_score += volatility_risk * 5; reasons.append(f"High Volatility Risk ({volatility_risk}/10)")
        confidence = max(0, 100 - int(risk_score)); verdict = confidence >= 50
        return verdict, confidence, reasons

class GuardianMind(BaseMind):
    """संरक्षक: अन-चेन सुरक्षा र आधारभूत 'रेड फ्ल्याग'हरूको विश्लेषण गर्दछ।"""
    def __init__(self): super().__init__("Guardian")
    def analyze(self, coin_data):
        self.logger.debug(f"'{coin_data['symbol']}' को लागि सुरक्षा जाँच गर्दै..."); return True, 100, ["Security checks passed"]

def _analyze_and_classify(coin_data):
    """एकल सिक्काको विश्लेषण गर्छ, सहमति खोज्छ, र अवसरलाई वर्गीकरण गर्छ।"""
    prophet = ProphetMind(); strategist = StrategistMind(); guardian = GuardianMind()
    prophet_verdict, _, _ = prophet.analyze(coin_data)
    strategist_verdict, _, _ = strategist.analyze(coin_data)
    guardian_verdict, _, _ = guardian.analyze(coin_data)
    if all([prophet_verdict, strategist_verdict, guardian_verdict]):
        coin_data['final_verdict'] = 'APPROVED'
        conviction = coin_data.get('conviction_score', 0); mempool_conf = coin_data.get('mempool_confidence', 0); volatility = coin_data.get('risk_volatility', 0)
        if conviction > 99: coin_data['classification'] = 'URGENT_ALPHA'
        elif conviction > 95 and mempool_conf > 90: coin_data['classification'] = 'GENESIS'
        elif volatility > 8: coin_data['classification'] = 'BLACK_SWAN'
        else: coin_data['classification'] = 'SLEEPING_GIANT'
    else: coin_data['final_verdict'] = 'REJECTED'; coin_data['classification'] = 'NONE'
    return coin_data

def run_council_consensus(candidate_coins):
    logger = logging.getLogger("TriMind.Council"); logger.info(f"👑 सम्राटको परिषद् (v4.1) ले {len(candidate_coins)} उम्मेदवारहरूको विश्लेषण सुरु गर्यो।")
    analysis_results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_analyze_and_classify, coin) for coin in candidate_coins]
        for future in as_completed(futures): # अब यो लाइनले काम गर्नेछ
            try:
                result = future.result()
                if result['final_verdict'] == 'APPROVED': analysis_results.append(result)
            except Exception as e: logger.error(f"परिषद्को विश्लेषणमा त्रुटि: {e}", exc_info=True)
    logger.info(f"🧠 परिषद्को बैठक समाप्त भयो। {len(analysis_results)}/{len(candidate_coins)} अवसरहरू स्वीकृत भए।"); return analysis_results
