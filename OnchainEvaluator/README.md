# DeFi Risk Sniffer 🔍

A natural language-powered DeFi protocol risk assessment tool that analyzes on-chain data and provides comprehensive risk evaluations.

## Features

- Natural language queries for protocol risk assessment
- Real-time data from DeFi Llama API
- On-chain data analysis from Base Network
- AI-powered risk analysis with detailed explanations
- Visual risk indicators (🟢/🟡/🔴)
- Comprehensive metrics dashboard

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Internet connection for API access

## Environment Setup

1. Create a `.env` file in the root directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

To get your OpenAI API key:
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with "sk-")

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd defi-risk-sniffer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- streamlit
- openai
- requests
- web3

## Running the Application

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter your query in natural language, for example:
   - "Is Uniswap safe?"
   - "What's the risk level of Aave?"
   - "Show me the safety analysis for Compound"

2. View the comprehensive risk analysis, including:
   - Risk score (🟢/🟡/🔴)
   - Total Value Locked (TVL)
   - 24h Volume
   - Security metrics
   - Market metrics
   - Detailed risk explanation

## Data Sources

- Protocol Data: DeFi Llama API
- On-chain Data: Base Network
- Risk Analysis: OpenAI GPT-4

## Architecture

The application consists of several key components:

- `app.py`: Main Streamlit interface
- `defi_llama.py`: DeFi Llama API integration
- `base_integration.py`: Base Network integration
- `risk_analyzer.py`: AI-powered risk analysis
- `utils.py`: Utility functions

## Troubleshooting

Common issues and solutions:

1. **API Key Error**: Ensure your OpenAI API key is correctly set in the `.env` file
2. **Protocol Not Found**: Check the protocol name spelling or try a more popular protocol
3. **Connection Error**: Verify your internet connection and API endpoint availability

## Development

For local development:

1. Create a `.streamlit/config.toml` with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

2. Install development dependencies:
```bash
pip install black pytest mypy
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For major changes, please open an issue first to discuss the proposed changes.
