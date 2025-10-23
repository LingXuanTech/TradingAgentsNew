# TradingAgents Quick Start Guide

This guide will help you get TradingAgents up and running in minutes.

## Prerequisites

- **Python 3.10+** (required)
- **OpenAI API Key** (minimum requirement)
- **Alpha Vantage API Key** (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file with your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key-here  # Optional
```

**Get free API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Alpha Vantage: https://www.alphavantage.co/support/#api-key

### 5. Verify Installation

```bash
python check_installation.py
```

This will verify all dependencies are installed correctly.

## Usage Options

TradingAgents provides three ways to interact with the system:

### Option 1: Web Dashboard (Recommended for Beginners)

The easiest way to get started with a modern, intuitive interface.

```bash
streamlit run web_app.py
```

Or use the helper script:

```bash
./start_webapp.sh
```

Then open your browser to: http://localhost:8501

**Features:**
- 📊 Visual dashboard with system overview
- ⚙️ Easy LLM configuration (no code needed)
- 🚀 Interactive trading execution
- 📈 Results viewer with charts
- 💾 Export results as JSON

### Option 2: Command-Line Interface (CLI)

For users who prefer terminal-based interaction with rich formatting.

```bash
python -m cli.main
```

**Features:**
- Interactive prompts for ticker and date selection
- Real-time progress display with Rich formatting
- Configurable LLM models and research depth
- Beautiful terminal UI

### Option 3: Python Script

For programmatic access and automation.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
final_state, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## Your First Trading Analysis

Let's run your first analysis using the Web Dashboard:

### Step 1: Start the Dashboard

```bash
streamlit run web_app.py
```

### Step 2: Configure LLM Settings (First Time Only)

1. Go to "⚙️ LLM Configuration"
2. Select "🤖 LLM Settings" tab
3. Choose models:
   - **LLM Provider**: OpenAI
   - **Deep Think LLM**: gpt-4o-mini (cost-effective)
   - **Quick Think LLM**: gpt-4o-mini
4. Click "💾 Save Configuration"

### Step 3: Run Trading Analysis

1. Go to "🚀 Trading Execution"
2. Enter a ticker: `NVDA`
3. Select a date: `2024-05-10`
4. Click "🚀 Start Trading Analysis"
5. Wait for analysis to complete (~2-5 minutes)
6. Review the comprehensive reports

### Step 4: View Results

The analysis includes:
- **Market Analysis**: Technical indicators and price patterns
- **Sentiment Analysis**: Social media sentiment
- **News Analysis**: Recent news impact assessment
- **Fundamentals**: Financial metrics and ratios
- **Research Debate**: Bull vs Bear perspectives
- **Risk Analysis**: Multi-perspective risk assessment
- **Final Decision**: BUY / SELL / HOLD with rationale

## Configuration Tips

### Cost Optimization

**For Testing/Development:**
```python
config["deep_think_llm"] = "gpt-4o-mini"  # ~$0.15 per 1M input tokens
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 1
```
**Estimated cost per analysis: $0.10-0.50**

**For Production/Research:**
```python
config["deep_think_llm"] = "o1-mini"  # Better reasoning
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 3  # More thorough debate
```
**Estimated cost per analysis: $1-5**

### Data Source Configuration

Configure in Web Dashboard → "⚙️ LLM Configuration" → "💾 Data Vendors":

**Free Option (No Alpha Vantage key):**
- Core Stock APIs: `yfinance`
- Technical Indicators: `yfinance`
- Fundamental Data: `yfinance` or `openai`
- News Data: `google` or `openai`

**Recommended (With Alpha Vantage key):**
- Core Stock APIs: `yfinance` (faster)
- Technical Indicators: `yfinance`
- Fundamental Data: `alpha_vantage` (more detailed)
- News Data: `alpha_vantage` (more reliable)

### Agent Parameters

- **Max Debate Rounds**: Number of bull/bear debates (1-3 recommended)
- **Max Risk Discussion Rounds**: Risk team discussions (1-2 recommended)
- **Max Recursion Limit**: Safety limit (default 100 is fine)

## Common Issues

### "ModuleNotFoundError: No module named 'streamlit'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"

**Solution:** Set up `.env` file
```bash
cp .env.example .env
# Edit .env with your API key
```

Or set in Web Dashboard → "⚙️ LLM Configuration" → "🔑 API Keys"

### "Rate limit exceeded" (Alpha Vantage)

**Solution:** 
- Wait a moment (free tier: 5 calls/min)
- Switch to `yfinance` for some data sources
- Upgrade to Alpha Vantage Premium

### Web Dashboard won't start

**Solution:** Check port 8501 is available
```bash
# Use a different port
streamlit run web_app.py --server.port 8502
```

### Slow execution

**Solutions:**
- Reduce debate rounds to 1
- Use `gpt-4o-mini` for both models
- Check internet connection
- Enable data caching

## Understanding Results

### Decision Types

- **BUY**: Agents recommend buying (bullish outlook)
- **SELL**: Agents recommend selling (bearish outlook)
- **HOLD**: Agents recommend holding position (neutral outlook)

### Confidence Levels

Results include reasoning from multiple perspectives:
- **Bull Researchers**: Optimistic analysis
- **Bear Researchers**: Pessimistic analysis
- **Risk Analysts**: Risk assessment
- **Portfolio Manager**: Final decision

### Interpreting Reports

1. **Market Analysis**: Look at technical indicators (RSI, MACD)
2. **News Analysis**: Check recent events and their impact
3. **Fundamentals**: Review financial health metrics
4. **Debate**: Understand both bull and bear arguments
5. **Risk**: Assess from multiple risk tolerance perspectives
6. **Final Decision**: Comprehensive synthesis

## Next Steps

### Backtesting

Run analysis on multiple dates:

```python
dates = ["2024-05-01", "2024-05-10", "2024-05-20"]
for date in dates:
    final_state, decision = ta.propagate("NVDA", date)
    # Store and analyze results
```

### Custom Configuration

Explore advanced options:
- Try different LLM providers (Anthropic, Google)
- Adjust debate rounds for quality vs cost
- Configure tool-level vendor overrides
- Customize data sources

### Multiple Tickers

Analyze a portfolio:

```python
tickers = ["NVDA", "AAPL", "TSLA", "MSFT"]
for ticker in tickers:
    final_state, decision = ta.propagate(ticker, "2024-05-10")
    # Aggregate results
```

### Reflection and Learning

Enable agent reflection on outcomes:

```python
# After knowing the actual outcome
returns = 150  # Profit/loss in dollars
ta.reflect_and_remember(returns)
```

## Learning Resources

- **Paper**: [arXiv:2412.20138](https://arxiv.org/abs/2412.20138)
- **Web Dashboard Guide**: [WEB_APP_README.md](./WEB_APP_README.md)
- **Discord Community**: [Join here](https://discord.com/invite/hk9PGKShPK)
- **GitHub Discussions**: [Ask questions](https://github.com/TauricResearch/TradingAgents/discussions)

## Support

Need help? We're here for you:

1. **Check Documentation**: Read README.md and WEB_APP_README.md
2. **Run Diagnostics**: `python check_installation.py`
3. **Discord**: Join our community for live help
4. **GitHub Issues**: Report bugs or request features

## Important Disclaimer

⚠️ **TradingAgents is for research purposes only.** Trading performance may vary based on many factors including model selection, temperature, data quality, and non-deterministic factors. **This is not financial, investment, or trading advice.**

Always:
- Do your own research
- Consult financial professionals
- Understand the risks
- Test thoroughly before any real trading

---

**Ready to start?** Run `streamlit run web_app.py` and explore! 🚀

**Questions?** Join our [Discord](https://discord.com/invite/hk9PGKShPK) 💬
