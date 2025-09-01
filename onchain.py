# onchain.py (The All-Seeing On-Chain Oracle v5.0 - Final)
import logging
import asyncio
import httpx
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

from omega_secrets import ONCHAIN_API_KEYS

# --- Chain Configuration ---
CHAIN_CONFIG = {
    "ethereum":  {"url": "https://api.etherscan.io/api", "name": "Ethereum"},
    "bsc":       {"url": "https://api.bscscan.com/api", "name": "BNB Smart Chain"},
    "polygon":   {"url": "https://api.polygonscan.com/api", "name": "Polygon"},
}

def _normalize_large_number(num_str: str, decimals: int = 18) -> float:
    """Converts a large integer string (like total supply) to a float."""
    try:
        return float(num_str) / (10 ** decimals)
    except (ValueError, TypeError):
        return 0.0

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=3, max=12))
async def _fetch_api(client: httpx.AsyncClient, chain: str, params: dict) -> Optional[Dict[str, Any]]:
    """A robust async function to fetch data from any Etherscan-family API with retries."""
    url = CHAIN_CONFIG[chain]["url"]
    try:
        response = await client.get(url, params=params, timeout=20)
        if response.status_code == 429: raise Exception(f"Rate limited on {chain}")
        response.raise_for_status()
        data = response.json()
        if str(data.get("status")) == "1":
            return data
        else:
            logging.warning(f"On-chain API for {chain} returned valid error: {data.get('result') or data.get('message')}")
            return None
    except Exception as e:
        logging.error(f"On-chain fetch for {chain} failed on last attempt: {e}")
        raise

async def get_onchain_metrics(platform: Optional[str], contract_address: Optional[str]) -> Dict[str, Any]:
    """
    The Ultimate On-Chain Sense. Fetches multiple critical on-chain metrics concurrently.
    """
    logger = logging.getLogger("OnChainOracle_v5")
    chain = platform.lower().replace(" ", "") if platform else None
    
    # --- Pre-flight Checks ---
    if not chain or not contract_address: return {"onchain_error": "Missing chain or address"}
    if chain not in CHAIN_CONFIG: return {"onchain_error": f"Unsupported chain: {chain}"}
    api_key = ONCHAIN_API_KEYS.get(chain)
    if not api_key: return {"onchain_error": f"Missing API Key for {chain}"}

    # --- Concurrent Task Definition ---
    async with httpx.AsyncClient() as client:
        tasks = {
            "holder_count": _fetch_api(client, chain, {"module": "token", "action": "tokenholder_count", "contractaddress": contract_address, "apikey": api_key}),
            "total_supply": _fetch_api(client, chain, {"module": "stats", "action": "tokensupply", "contractaddress": contract_address, "apikey": api_key}),
            "contract_verified": _fetch_api(client, chain, {"module": "contract", "action": "getabi", "address": contract_address, "apikey": api_key}),
            # Placeholder for a more complex whale transaction fetch
            "whale_activity": asyncio.sleep(0, result={"result": "Module Offline"}),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
    # --- Process and Normalize Results ---
    results_dict = dict(zip(tasks.keys(), results))
    final_metrics = {"onchain_error": []}

    # Holder Count
    if isinstance(r := results_dict.get("holder_count"), dict): final_metrics["holder_count"] = int(r.get("result", 0))
    else: final_metrics["onchain_error"].append("HolderCountFailed")

    # Total Supply (Normalized)
    if isinstance(r := results_dict.get("total_supply"), dict): final_metrics["total_supply"] = _normalize_large_number(r.get("result", "0"))
    else: final_metrics["onchain_error"].append("TotalSupplyFailed")

    # Contract Verification
    if isinstance(r := results_dict.get("contract_verified"), dict):
        final_metrics["is_verified"] = "Yes" if r.get("result") != "Contract source code not verified" else "No"
    else: final_metrics["onchain_error"].append("VerificationCheckFailed")
        
    # Whale Activity (Placeholder)
    final_metrics["whale_activity_status"] = results_dict["whale_activity"]["result"]
    
    # Join errors into a string
    final_metrics["onchain_error"] = ", ".join(final_metrics["onchain_error"]) if final_metrics["onchain_error"] else None

    logger.info(f"On-chain metrics for {contract_address[:10]}... on {chain}: {final_metrics}")
    return final_metrics
