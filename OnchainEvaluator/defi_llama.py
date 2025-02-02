import requests
import time
from typing import Dict, Any

class RateLimiter:
    def __init__(self, calls_per_second=2):
        self.calls_per_second = calls_per_second
        self.last_call = 0

    def wait(self):
        current_time = time.time()
        time_since_last_call = current_time - self.last_call
        if time_since_last_call < (1 / self.calls_per_second):
            time.sleep((1 / self.calls_per_second) - time_since_last_call)
        self.last_call = time.time()

class DefiLlamaAPI:
    BASE_URL = "https://api.llama.fi"

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.session = requests.Session()

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        self.rate_limiter.wait()
        response = self.session.get(f"{self.BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()

    def _normalize_protocol_name(self, name: str) -> str:
        """Normalize protocol name for matching"""
        return name.lower().replace(' ', '').replace('-', '').replace('_', '')

    def get_protocol(self, protocol_name: str) -> Dict[str, Any]:
        try:
            protocols = self._make_request("/protocols")
            normalized_search = self._normalize_protocol_name(protocol_name)

            # Try exact match first
            protocol = next(
                (p for p in protocols 
                 if self._normalize_protocol_name(p["name"]) == normalized_search),
                None
            )

            # If no exact match, try partial match
            if not protocol:
                protocol = next(
                    (p for p in protocols 
                     if normalized_search in self._normalize_protocol_name(p["name"])),
                    None
                )

            if not protocol:
                raise ValueError(
                    f"Protocol '{protocol_name}' not found. Please check the protocol name and try again."
                )

            return protocol
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to DeFi Llama API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching protocol data: {str(e)}")

def get_protocol_data(protocol_name: str) -> Dict[str, Any]:
    """
    Fetch and process protocol data from DeFi Llama
    """
    api = DefiLlamaAPI()
    try:
        protocol = api.get_protocol(protocol_name)

        # Process and standardize the data
        return {
            'name': protocol.get('name', ''),
            'tvl': protocol.get('tvl', 0),
            'volume_24h': protocol.get('volume24h', 0),
            'audit_status': 'Audited' if protocol.get('audit', False) else 'Unaudited',
            'contract_age': protocol.get('age', 'Unknown'),
            'liquidity_score': min(10, round(protocol.get('tvl', 0) / 1000000)),  # Simplified scoring
            'market_dominance': round(protocol.get('dominance', 0) * 100, 2),
            'chain': protocol.get('chain', 'Unknown'),
            'category': protocol.get('category', 'Unknown')
        }
    except Exception as e:
        raise Exception(f"Failed to fetch protocol data: {str(e)}")