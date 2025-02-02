import os
import json
from typing import Dict, Any
from openai import OpenAI

# Use the latest GPT-4 model
MODEL = "gpt-3.5-turbo"


class RiskAnalyzer:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_risk(self, protocol_data: Dict[str, Any],
                     onchain_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze protocol risk using protocol data and AI
        """
        prompt = self._create_analysis_prompt(protocol_data, onchain_data)

        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a DeFi risk analysis expert. Analyze the protocol data and provide a risk assessment."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                response_format={"type": "json_object"})

            result = json.loads(response.choices[0].message.content)
            return self._process_risk_score(result, protocol_data)
        except Exception as e:
            raise Exception(f"Error in risk analysis: {str(e)}")

    def _create_analysis_prompt(self, protocol_data: Dict[str, Any],
                                onchain_data: Dict[str, Any]) -> str:
        return f"""
        Analyze the following DeFi protocol data and provide a risk assessment:

        Protocol: {protocol_data['name']}
        TVL: ${protocol_data['tvl']:,}
        24h Volume: ${protocol_data['volume_24h']:,}
        Audit Status: {protocol_data['audit_status']}
        Contract Age: {protocol_data['contract_age']}
        Market Dominance: {protocol_data['market_dominance']}%
        Category: {protocol_data['category']}

        Onchain Metrics:
        - Active Users: {onchain_data['active_users']}
        - Transaction Volume: {onchain_data['transaction_volume']}
        - Smart Contract Interactions: {onchain_data['contract_interactions']}

        Provide a risk assessment in JSON format with the following structure:
        {{
            "risk_level": "High|Medium|Low",
            "risk_score": "🔴|🟡|🟢",
            "explanation": "Detailed explanation of the risk assessment"
        }}
        """

    def _process_risk_score(self, ai_result: Dict[str, Any],
                            protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the AI risk analysis and combine with protocol metrics
        """
        risk_mapping = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

        try:
            # Ensure risk_level is valid
            if ai_result['risk_level'] not in risk_mapping:
                ai_result['risk_level'] = "Medium"
                ai_result['risk_score'] = "🟡"

            # Add protocol metadata
            ai_result['protocol_name'] = protocol_data['name']
            ai_result['tvl'] = protocol_data['tvl']
            return ai_result
        except Exception as e:
            raise Exception(f"Error processing risk score: {str(e)}")


def analyze_protocol_risk(protocol_name: str, defi_data: Dict[str, Any],
                          onchain_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to analyze protocol risk
    """
    analyzer = RiskAnalyzer()
    return analyzer.analyze_risk(defi_data, onchain_data)
