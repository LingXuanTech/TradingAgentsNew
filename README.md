<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: 多智能体LLM智能交易平台

> 🎉 **TradingAgents v2.0** 正式发布！感谢社区的热情支持，我们决定完全开源这个先进的智能交易框架。
>
> 新版本带来了革命性的多LLM供应商支持、企业级前端界面、生产就绪的完整解决方案！

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
    <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
  </picture>
</a>
</div>

<div align="center">

🚀 [快速开始](#快速开始) | 📊 [核心功能](#核心功能) | ⚙️ [安装配置](#安装配置) | 🌐 [双前端界面](#双前端界面) | 🤖 [多LLM系统](#多llm系统) | 🏦 [经纪商集成](#经纪商集成) | 📚 [完整手册](#完整手册)

</div>

## 🎯 核心功能概览

TradingAgents是一个革命性的多智能体LLM智能交易平台，具备以下核心特性：

### 🤖 多智能体协作系统
- **分析师团队**: 技术分析、基本面分析、新闻分析、社交媒体情绪分析
- **研究员团队**: 看涨/看跌研究员辩论，形成投资共识
- **决策团队**: 交易员制定策略，风险管理审核决策
- **智能分工**: 每个智能体专注于特定领域，优势互补

### 🚀 多LLM供应商支持
- **个性化配置**: 为每个智能体分配最适合的LLM模型
- **供应商多样性**: 支持OpenAI、Anthropic、Google、本地部署等
- **智能分配**: 研究员用o1-preview深度思考，分析师用gpt-4o快速分析
- **企业级监控**: LLM性能监控、成本控制、故障恢复

### 🌐 双前端界面选择
- **Streamlit现代化界面**: shadcn/ui组件，交互丰富
- **Flask专业界面**: 传统Web界面，稳定可靠
- **实时数据更新**: WebSocket毫秒级数据推送
- **响应式设计**: 完美适配桌面、平板、手机

### 📊 高级技术分析
- **40+技术指标**: 趋势、动量、波动率、成交量全覆盖
- **智能信号生成**: 自动生成买卖信号和投资建议
- **形态识别**: 自动识别经典技术形态
- **多数据源**: Alpha Vantage、yfinance、Google News等

### 🏦 经纪商API集成
- **多平台支持**: 华泰证券、广发证券等主流券商
- **沙箱测试**: 安全的测试环境，保护真实资金
- **异步架构**: 高性能非阻塞API调用
- **统一接口**: 标准化经纪商接口，易于扩展

### ⏰ 自动化交易引擎
- **定时调度**: 灵活的交易时间和频率配置
- **市场监控**: 实时价格监控和异常检测
- **风险控制**: 多层次风险管理和止损机制
- **邮件通知**: 交易提醒、风险预警、日报表

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> ⚠️ **重要声明**: TradingAgents框架专为研究目的而设计。交易性能受多种因素影响，包括所选语言模型、模型温度、交易周期、数据质量等非确定性因素。[本系统不作为金融、投资或交易建议使用。](https://tauric.ai/disclaimer/)

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installation and CLI

### Installation

Clone TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Create a virtual environment in any of your favorite environment managers:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration Setup

TradingAgents uses a unified configuration system for easy management:

1. **Copy configuration template:**
```bash
cp tradingagents/config/user_config_template.yaml tradingagents/config/user_config.yaml
```

2. **Edit configuration:**
```bash
# Edit the user_config.yaml file with your settings
nano tradingagents/config/user_config.yaml
```

3. **Configure API credentials:**
   - Add your broker API keys (Huatai, Guangfa, etc.)
   - Set up email notification settings
   - Configure multi-agent LLM settings
   - Customize trading parameters and risk management rules

4. **Validate configuration:**
```python
from tradingagents.config.config_manager import validate_config
errors = validate_config()
if errors:
    print("Configuration errors:", errors)
else:
    print("Configuration is valid!")
```

### Multi-Agent LLM Configuration

TradingAgents supports different LLM providers for different agents:

```yaml
llm:
  # Researchers use o1-preview for deep thinking
  researchers:
    provider: "openai"
    model: "o1-preview"
    temperature: 0.8
    max_tokens: 4096

  # Analysts use gpt-4o for fast analysis
  analysts:
    provider: "openai"
    model: "gpt-4o"
    temperature: 0.3
    max_tokens: 2048

  # Risk managers use conservative settings
  risk_manager:
    provider: "openai"
    model: "gpt-4o"
    temperature: 0.1
    max_tokens: 2048
```

Supported providers: OpenAI, Anthropic, Google, Ollama, OpenRouter

### Modern Web Interface (Streamlit + shadcn/ui)

TradingAgents now includes a modern web interface built with Streamlit and shadcn/ui:

```bash
# Launch the modern web interface
python tradingagents/streamlit_app/run.py

# Or run directly with streamlit
streamlit run tradingagents/streamlit_app/app.py
```

**Features:**
- 🎨 Modern UI with shadcn/ui components
- 📊 Real-time trading dashboard
- 💹 Interactive trading interface
- 🛡️ Risk management panel
- 📈 Technical analysis charts
- ⚙️ System configuration panel

**Access:** http://localhost:8501

### Required APIs

You will need the OpenAI API for all the agents, and [Alpha Vantage API](https://www.alphavantage.co/support/#api-key) for fundamental and news data (default configuration).

```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
export ALPHA_VANTAGE_API_KEY=$YOUR_ALPHA_VANTAGE_API_KEY
```

Alternatively, you can create a `.env` file in the project root with your API keys (see `.env.example` for reference):
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

**Note:** We are happy to partner with Alpha Vantage to provide robust API support for TradingAgents. You can get a free AlphaVantage API [here](https://www.alphavantage.co/support/#api-key), TradingAgents-sourced requests also have increased rate limits to 60 requests per minute with no daily limits. Typically the quota is sufficient for performing complex tasks with TradingAgents thanks to Alpha Vantage’s open-source support program. If you prefer to use OpenAI for these data sources instead, you can modify the data vendor settings in `tradingagents/default_config.py`.

### CLI Usage

You can also try out the CLI directly by running:
```bash
python -m cli.main
```
You will see a screen where you can select your desired tickers, date, LLMs, research depth, etc.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents Package

### Implementation Details

We built TradingAgents with LangGraph to ensure flexibility and modularity. We utilize `o1-preview` and `gpt-4o` as our deep thinking and fast thinking LLMs for our experiments. However, for testing purposes, we recommend you use `o4-mini` and `gpt-4.1-mini` to save on costs as our framework makes **lots of** API calls.

### Python Usage

To use TradingAgents inside your code, you can import the `tradingagents` module and initialize a `TradingAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds

# Configure data vendors (default uses yfinance and Alpha Vantage)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: yfinance, alpha_vantage, local
    "technical_indicators": "yfinance",      # Options: yfinance, alpha_vantage, local
    "fundamental_data": "alpha_vantage",     # Options: openai, alpha_vantage, local
    "news_data": "alpha_vantage",            # Options: openai, alpha_vantage, google, local
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

> The default configuration uses yfinance for stock price and technical data, and Alpha Vantage for fundamental and news data. For production use or if you encounter rate limits, consider upgrading to [Alpha Vantage Premium](https://www.alphavantage.co/premium/) for more stable and reliable data access. For offline experimentation, there's a local data vendor option that uses our **Tauric TradingDB**, a curated dataset for backtesting, though this is still in development. We're currently refining this dataset and plan to release it soon alongside our upcoming projects. Stay tuned!

You can view the full list of configurations in `tradingagents/default_config.py`.

## Contributing

We welcome contributions from the community! Whether it's fixing a bug, improving documentation, or suggesting a new feature, your input helps make this project better. If you are interested in this line of research, please consider joining our open-source financial AI research community [Tauric Research](https://tauric.ai/).

## Citation

Please reference our work if you find *TradingAgents* provides you with some help :)

```
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
