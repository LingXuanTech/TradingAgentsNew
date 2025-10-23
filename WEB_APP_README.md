# TradingAgents Web Dashboard

A comprehensive web interface for the TradingAgents multi-agent LLM trading framework. The dashboard provides an intuitive interface for configuration, execution, and analysis of trading decisions.

## Features

### 🏠 Dashboard
- Overview of the multi-agent architecture
- Real-time system status and metrics
- Trading history visualization
- Agent status monitoring

### ⚙️ LLM Configuration
- **LLM Settings**: Configure language model providers (OpenAI, Anthropic, Google, etc.)
- **Model Selection**: Choose deep thinking and quick thinking models
- **Data Vendors**: Configure data sources for market data, news, and fundamentals
- **Agent Parameters**: Adjust debate rounds, recursion limits, and other behaviors
- **API Keys**: Secure API key management

### 🚀 Trading Execution
- Execute trading analysis for any ticker and date
- Real-time progress monitoring
- Detailed analysis reports from all agent teams
- View debate histories and decision rationale
- Export results in JSON format

### 📊 Results Viewer
- Browse historical trading results
- Filter by ticker, date range
- Visualize decision distributions
- View detailed analysis reports
- Export historical data

### ℹ️ About
- Framework documentation
- Agent team descriptions
- Citation information
- Links to resources

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file with your API keys:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required API keys:
- `OPENAI_API_KEY`: For OpenAI models (required by default)
- `ALPHA_VANTAGE_API_KEY`: For market data (optional but recommended)
- `ANTHROPIC_API_KEY`: For Claude models (optional)
- `GOOGLE_API_KEY`: For Gemini models (optional)

### 3. Run the Web App

```bash
streamlit run web_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Usage Guide

### First Time Setup

1. **Configure API Keys**
   - Navigate to "⚙️ LLM Configuration" → "🔑 API Keys"
   - Enter your OpenAI API key (minimum requirement)
   - Optionally add Alpha Vantage key for better data access

2. **Configure LLM Settings**
   - Go to "🤖 LLM Settings" tab
   - Select your LLM provider (default: OpenAI)
   - Choose models:
     - For testing: `gpt-4o-mini` for both (cost-effective)
     - For production: `o1-mini` (deep) + `gpt-4o-mini` (quick)

3. **Configure Data Sources**
   - Go to "💾 Data Vendors" tab
   - Recommended settings:
     - Core Stock APIs: `yfinance` (free)
     - Technical Indicators: `yfinance` (free)
     - Fundamental Data: `alpha_vantage` (requires API key)
     - News Data: `alpha_vantage` (requires API key)

### Running a Trading Analysis

1. Navigate to "🚀 Trading Execution"
2. Enter a stock ticker (e.g., `NVDA`, `AAPL`, `TSLA`)
3. Select the analysis date
4. Optional: Enable debug mode for detailed logging
5. Click "🚀 Start Trading Analysis"
6. Monitor real-time progress as agents analyze the stock
7. Review the comprehensive reports:
   - Market Analysis (Technical indicators)
   - Sentiment Analysis (Social media sentiment)
   - News Analysis (Recent news impact)
   - Fundamentals (Financial metrics)
   - Research Debate (Bull vs Bear perspectives)
   - Risk Analysis (Multi-perspective risk assessment)
8. Download results in JSON format

### Viewing Historical Results

1. Navigate to "📊 Results Viewer"
2. Filter results by ticker or date range
3. View decision distribution charts
4. Select a specific result for detailed analysis
5. Export results as needed

## Configuration Options

### LLM Providers

The dashboard supports multiple LLM providers:

- **OpenAI**: GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **Anthropic**: Claude 3 Opus, Sonnet, Haiku
- **Google**: Gemini 1.5 Pro, Flash
- **Ollama**: Local models (Llama, Mistral, etc.)
- **OpenRouter**: Various models via OpenRouter API

### Data Vendors

Choose data sources based on your needs:

- **yfinance**: Free, no API key required, good for basic data
- **alpha_vantage**: Free tier available, better for fundamentals and news
- **openai**: Use LLM for data analysis (experimental)
- **google**: Google search for news (experimental)
- **local**: Use cached data (for offline testing)

### Agent Parameters

Fine-tune agent behavior:

- **Max Debate Rounds**: Number of bull/bear debate rounds (1-10)
  - More rounds = better analysis but higher cost
  - Recommended: 1-2 for testing, 3-5 for production
- **Max Risk Discussion Rounds**: Risk team discussion rounds (1-10)
- **Max Recursion Limit**: Safety limit for graph execution (10-500)

## Cost Optimization Tips

1. **For Testing/Development**:
   - Use `gpt-4o-mini` for both deep and quick thinking
   - Set debate rounds to 1
   - Use `yfinance` for all data sources
   - Estimated cost: ~$0.10-0.50 per analysis

2. **For Production/Research**:
   - Use `o1-mini` for deep thinking, `gpt-4o-mini` for quick
   - Set debate rounds to 2-3
   - Use `alpha_vantage` for fundamentals and news
   - Estimated cost: ~$1-5 per analysis

3. **Cost Reduction Strategies**:
   - Cache frequently accessed data
   - Use local data vendor for backtesting
   - Reduce debate rounds for less critical decisions
   - Use smaller models for quick thinking tasks

## Troubleshooting

### "OpenAI API key not found"
- Go to "⚙️ LLM Configuration" → "🔑 API Keys"
- Enter your OpenAI API key
- Or set `OPENAI_API_KEY` in your `.env` file

### "Rate limit exceeded"
- Alpha Vantage free tier: 5 calls/minute, 500 calls/day
- Solution: Wait a moment or upgrade to premium
- Alternative: Switch to `yfinance` for some data sources

### "Connection timeout"
- Check your internet connection
- Verify API keys are correct
- Try increasing timeout in advanced settings

### Results not showing
- Check `eval_results/` directory exists
- Ensure write permissions
- Verify results_dir in configuration

### Slow execution
- Reduce debate rounds
- Use faster models (gpt-4o-mini)
- Enable caching for data sources
- Check network latency

## Architecture

The web dashboard is built with:

- **Streamlit**: Web framework for the UI
- **Plotly**: Interactive visualizations
- **TradingAgentsGraph**: Core trading logic
- **LangChain/LangGraph**: LLM orchestration

### Agent Flow

```
1. Analyst Team (Parallel)
   ├─ Market Analyst → Technical analysis
   ├─ Social Analyst → Sentiment analysis  
   ├─ News Analyst → News impact
   └─ Fundamentals Analyst → Financial metrics

2. Research Team (Sequential debate)
   ├─ Bull Researcher ←→ Bear Researcher
   └─ Research Manager → Synthesis

3. Trading Team
   └─ Trader → Investment plan

4. Risk Management Team (Parallel + Discussion)
   ├─ Risky Analyst
   ├─ Neutral Analyst
   ├─ Safe Analyst
   └─ Portfolio Manager → Final decision
```

## Security Notes

⚠️ **Important Security Considerations**:

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` file for sensitive data
3. **Session State**: Keys entered in UI are temporary (session only)
4. **Production**: Use proper secret management for production deployments
5. **Network**: Use HTTPS in production environments

## Contributing

Contributions are welcome! Areas for improvement:

- Additional data source integrations
- More visualization options
- Real-time streaming execution updates
- Backtesting functionality
- Portfolio management features
- Performance analytics
- A/B testing of different configurations

## License

This project is part of the TradingAgents framework and follows the same MIT license.

## Support

- **Issues**: [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
- **Discord**: [Join our community](https://discord.com/invite/hk9PGKShPK)
- **Documentation**: [Main README](./README.md)

## Citation

If you use this web dashboard in your research, please cite the TradingAgents paper:

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

---

**Built with ❤️ by the TradingAgents team**
