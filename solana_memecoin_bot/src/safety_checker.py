import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_token_safety(token_address, config):
    """Check token safety on RugCheck.xyz."""
    url = f"https://rugcheck.xyz/tokens/{token_address}"  # Mock URL
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logger.error(f"RugCheck failed for {token_address}: {response.status_code}")
            return None
        
        # Mock parsing (replace with real API or scraping logic)
        soup = BeautifulSoup(response.text, 'html.parser')
        safety_score = float(soup.find(id="safety-score").text or 0)  # Hypothetical
        liquidity_burned = "burned" in (soup.find(id="liquidity-status").text or "").lower()
        mintable = "mintable" in (soup.find(id="token-flags").text or "").lower()
        pausable = "pausable" in (soup.find(id="token-flags").text or "").lower()

        return {
            "safety_score": safety_score,
            "liquidity_burned": liquidity_burned,
            "mintable": mintable,
            "pausable": pausable
        }
    except Exception as e:
        logger.error(f"Error checking {token_address} on RugCheck: {e}")
        return None

def is_safe_token(token_address, config):
    """Determine if a token meets safety criteria."""
    safety_data = check_token_safety(token_address, config)
    if not safety_data:
        return False
    return (safety_data["safety_score"] >= config["filters"]["min_safety_score"] and 
            safety_data["liquidity_burned"] and 
            not safety_data["mintable"] and 
            not safety_data["pausable"])
