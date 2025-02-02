from typing import Dict, Any
from web3 import Web3
import os

class BaseChainIntegration:
    def __init__(self):
        # Base Sepolia testnet RPC URL
        self.w3 = Web3(Web3.HTTPProvider('https://sepolia.base.org'))
        
    def get_protocol_data(self, protocol_address: str) -> Dict[str, Any]:
        """
        Fetch protocol data from Base Sepolia testnet
        """
        try:
            # Basic metrics
            block_number = self.w3.eth.block_number
            
            # Get last 1000 blocks of data
            active_users = set()
            transaction_count = 0
            
            for block in range(block_number - 1000, block_number):
                block_data = self.w3.eth.get_block(block, full_transactions=True)
                for tx in block_data.transactions:
                    if tx['to'] and tx['to'].lower() == protocol_address.lower():
                        active_users.add(tx['from'])
                        transaction_count += 1
            
            return {
                'active_users': len(active_users),
                'transaction_volume': transaction_count,
                'contract_interactions': transaction_count
            }
        except Exception as e:
            # Return default values if chain data cannot be fetched
            return {
                'active_users': 0,
                'transaction_volume': 0,
                'contract_interactions': 0
            }

def get_onchain_data(protocol_name: str) -> Dict[str, Any]:
    """
    Get protocol data from Base Sepolia testnet
    """
    # Mock data for demonstration - in production, would need protocol address mapping
    return {
        'active_users': 1500,
        'transaction_volume': 25000,
        'contract_interactions': 12000
    }
