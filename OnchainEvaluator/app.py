import streamlit as st
import time
from defi_llama import get_protocol_data
from risk_analyzer import analyze_protocol_risk
from base_integration import get_onchain_data
from utils import format_currency

st.set_page_config(
    page_title="DeFi Risk Sniffer",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .risk-score {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🔍 DeFi Risk Sniffer")
    st.markdown("""
        Ask about any DeFi protocol's risk level using natural language.
        We'll analyze on-chain data and provide a comprehensive risk assessment.
    """)

    # User input
    user_query = st.text_input(
        "Ask about a protocol's safety (e.g., 'Is Uniswap safe?')",
        placeholder="Enter your question here..."
    )

    if user_query:
        with st.spinner("🔍 Analyzing protocol risk..."):
            try:
                # Extract protocol name from query
                protocol_name = user_query.lower().replace("is ", "").replace(" safe?", "").strip()
                
                # Get protocol data
                defi_data = get_protocol_data(protocol_name)
                onchain_data = get_onchain_data(protocol_name)
                
                # Analyze risk
                risk_result = analyze_protocol_risk(protocol_name, defi_data, onchain_data)
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"<div class='risk-score'>{risk_result['risk_score']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center'>{risk_result['risk_level']}</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric("Total Value Locked", format_currency(defi_data['tvl']))
                    st.markdown("</div>", unsafe_allow_html=True)

                with col3:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric("24h Volume", format_currency(defi_data['volume_24h']))
                    st.markdown("</div>", unsafe_allow_html=True)

                # Detailed metrics
                st.subheader("Detailed Risk Analysis")
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.write("🔒 Security Metrics")
                    st.write(f"- Audit Status: {defi_data['audit_status']}")
                    st.write(f"- Smart Contract Age: {defi_data['contract_age']}")
                    st.markdown("</div>", unsafe_allow_html=True)

                with metrics_col2:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.write("📊 Market Metrics")
                    st.write(f"- Liquidity Score: {defi_data['liquidity_score']}/10")
                    st.write(f"- Market Dominance: {defi_data['market_dominance']}%")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Risk explanation
                st.markdown("### Risk Assessment Details")
                st.write(risk_result['explanation'])

            except Exception as e:
                st.error(f"Error analyzing protocol: {str(e)}")
                st.write("Please try another protocol or rephrase your question.")

    # Footer
    st.markdown("---")
    st.markdown("Powered by Base Network • DeFi Llama API • OpenAI")

if __name__ == "__main__":
    main()
