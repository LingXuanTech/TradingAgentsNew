"""
TradingAgents Web Dashboard
A comprehensive web interface for the TradingAgents framework with dashboard and LLM configuration.
"""

import streamlit as st
import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TradingAgents Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-pending {
        background-color: #f3f4f6;
        border-left: 4px solid #9ca3af;
    }
    .status-running {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    .status-completed {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
    }
    .status-error {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = DEFAULT_CONFIG.copy()
if 'trading_history' not in st.session_state:
    st.session_state.trading_history = []
if 'current_execution' not in st.session_state:
    st.session_state.current_execution = None
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {}


def load_trading_results() -> List[Dict[str, Any]]:
    """Load trading results from eval_results directory"""
    results: List[Dict[str, Any]] = []
    results_dir = Path("eval_results")
    if results_dir.exists():
        for ticker_dir in results_dir.iterdir():
            if ticker_dir.is_dir():
                logs_dir = ticker_dir / "TradingAgentsStrategy_logs"
                if logs_dir.exists():
                    for log_file in logs_dir.glob("full_states_log_*.json"):
                        try:
                            with open(log_file, 'r') as f:
                                data = json.load(f)
                                for date, state in data.items():
                                    results.append({
                                        'ticker': ticker_dir.name,
                                        'date': date,
                                        'decision': state.get('final_trade_decision', 'N/A'),
                                        'file': str(log_file)
                                    })
                        except Exception as e:
                            st.error(f"Error loading {log_file}: {e}")
    return results


def render_sidebar() -> str:
    """Render sidebar navigation"""
    with st.sidebar:
        st.image("assets/TauricResearch.png", use_container_width=True)
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "⚙️ LLM Configuration", "🚀 Trading Execution", "📊 Results Viewer", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        
        # Show some quick stats
        results = load_trading_results()
        st.metric("Total Trades", len(results))
        
        if results:
            df = pd.DataFrame(results)
            st.metric("Unique Tickers", df['ticker'].nunique())
        
        st.markdown("---")
        st.markdown("### API Status")
        
        # Check API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        
        if openai_key:
            st.success("✓ OpenAI API")
        else:
            st.error("✗ OpenAI API")
            
        if alpha_vantage_key:
            st.success("✓ Alpha Vantage API")
        else:
            st.warning("⚠ Alpha Vantage API")
        
        return page


def render_dashboard() -> None:
    """Render main dashboard"""
    st.markdown('<div class="main-header">TradingAgents Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent LLM Financial Trading Framework")
    
    # Load trading results
    results = load_trading_results()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Executions", len(results))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if results:
            df = pd.DataFrame(results)
            st.metric("Unique Tickers", df['ticker'].nunique())
        else:
            st.metric("Unique Tickers", 0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Agents", 13)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        current_llm = st.session_state.config.get('quick_think_llm', 'N/A')
        st.metric("Current LLM", current_llm.split('-')[0])
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Agent Architecture Overview
    st.markdown("### Agent Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Analyst Team")
        analysts = [
            ("📊", "Market Analyst", "Technical analysis & indicators"),
            ("💬", "Social Analyst", "Sentiment analysis"),
            ("📰", "News Analyst", "News & macro events"),
            ("📈", "Fundamentals Analyst", "Financial statements & metrics")
        ]
        
        for icon, name, desc in analysts:
            with st.expander(f"{icon} {name}"):
                st.write(desc)
        
        st.markdown("#### Research Team")
        researchers = [
            ("🐂", "Bull Researcher", "Optimistic perspective"),
            ("🐻", "Bear Researcher", "Pessimistic perspective"),
            ("👨‍💼", "Research Manager", "Synthesizes debate")
        ]
        
        for icon, name, desc in researchers:
            with st.expander(f"{icon} {name}"):
                st.write(desc)
    
    with col2:
        st.markdown("#### Trading Team")
        with st.expander("💼 Trader"):
            st.write("Executes trading decisions based on research")
        
        st.markdown("#### Risk Management Team")
        risk_team = [
            ("⚠️", "Risky Analyst", "High risk tolerance view"),
            ("⚖️", "Neutral Analyst", "Balanced risk view"),
            ("🛡️", "Safe Analyst", "Conservative risk view"),
            ("👔", "Portfolio Manager", "Final decision maker")
        ]
        
        for icon, name, desc in risk_team:
            with st.expander(f"{icon} {name}"):
                st.write(desc)
    
    st.markdown("---")
    
    # Recent Trading History
    st.markdown("### Recent Trading History")
    
    if results:
        df = pd.DataFrame(results)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False).head(10)
        
        st.dataframe(
            df[['ticker', 'date', 'decision']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No trading history available. Start a new execution to see results here.")


def render_llm_config() -> None:
    """Render LLM configuration page"""
    st.markdown('<div class="main-header">LLM Configuration</div>', unsafe_allow_html=True)
    st.markdown("Configure the language models and parameters for the trading agents.")
    
    # Create tabs for different configuration sections
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 LLM Settings", "💾 Data Vendors", "🔧 Agent Parameters", "🔑 API Keys"])
    
    with tab1:
        st.markdown("### Language Model Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Provider Configuration")
            
            llm_provider = st.selectbox(
                "LLM Provider",
                ["openai", "anthropic", "google", "ollama", "openrouter"],
                index=["openai", "anthropic", "google", "ollama", "openrouter"].index(
                    st.session_state.config.get("llm_provider", "openai")
                ),
                help="Select your LLM provider"
            )
            st.session_state.config["llm_provider"] = llm_provider
            
            backend_url = st.text_input(
                "Backend URL",
                value=st.session_state.config.get("backend_url", "https://api.openai.com/v1"),
                help="API endpoint URL"
            )
            st.session_state.config["backend_url"] = backend_url
        
        with col2:
            st.markdown("#### Model Selection")
            
            if llm_provider == "openai":
                deep_models = ["o1-preview", "o1-mini", "o3-mini", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
                quick_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
            elif llm_provider == "anthropic":
                deep_models = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-5-sonnet-20241022"]
                quick_models = ["claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-5-sonnet-20241022"]
            elif llm_provider == "google":
                deep_models = ["gemini-1.5-pro", "gemini-1.5-flash"]
                quick_models = ["gemini-1.5-flash", "gemini-1.0-pro"]
            else:
                deep_models = ["llama3", "mistral", "mixtral"]
                quick_models = ["llama3", "mistral", "mixtral"]
            
            deep_think_llm = st.selectbox(
                "Deep Thinking LLM",
                deep_models,
                help="Model for complex reasoning tasks (Research, Risk Analysis)"
            )
            st.session_state.config["deep_think_llm"] = deep_think_llm
            
            quick_think_llm = st.selectbox(
                "Quick Thinking LLM",
                quick_models,
                help="Model for faster tasks (Data analysis, Report generation)"
            )
            st.session_state.config["quick_think_llm"] = quick_think_llm
        
        st.markdown("---")
        
        st.info("💡 **Recommendation**: Use `gpt-4o-mini` for both models during testing to minimize API costs. For production, consider `o1-mini` for deep thinking and `gpt-4o-mini` for quick thinking.")
    
    with tab2:
        st.markdown("### Data Vendor Configuration")
        st.markdown("Configure data sources for different types of market data.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Core Data Sources")
            
            core_stock_apis = st.selectbox(
                "Core Stock APIs",
                ["yfinance", "alpha_vantage", "local"],
                index=["yfinance", "alpha_vantage", "local"].index(
                    st.session_state.config["data_vendors"].get("core_stock_apis", "yfinance")
                ),
                help="Source for basic stock price data"
            )
            
            technical_indicators = st.selectbox(
                "Technical Indicators",
                ["yfinance", "alpha_vantage", "local"],
                index=["yfinance", "alpha_vantage", "local"].index(
                    st.session_state.config["data_vendors"].get("technical_indicators", "yfinance")
                ),
                help="Source for technical analysis indicators (MACD, RSI, etc.)"
            )
        
        with col2:
            st.markdown("#### Analysis Data Sources")
            
            fundamental_data = st.selectbox(
                "Fundamental Data",
                ["alpha_vantage", "openai", "local"],
                index=["alpha_vantage", "openai", "local"].index(
                    st.session_state.config["data_vendors"].get("fundamental_data", "alpha_vantage")
                ),
                help="Source for company fundamentals and financials"
            )
            
            news_data = st.selectbox(
                "News Data",
                ["alpha_vantage", "openai", "google", "local"],
                index=["alpha_vantage", "openai", "google", "local"].index(
                    st.session_state.config["data_vendors"].get("news_data", "alpha_vantage")
                ),
                help="Source for news and sentiment data"
            )
        
        st.session_state.config["data_vendors"] = {
            "core_stock_apis": core_stock_apis,
            "technical_indicators": technical_indicators,
            "fundamental_data": fundamental_data,
            "news_data": news_data,
        }
        
        st.markdown("---")
        
        st.markdown("#### Tool-Level Overrides")
        st.markdown("Override specific tools to use different vendors (optional)")
        
        with st.expander("Advanced: Tool Vendor Overrides"):
            tool_override_key = st.text_input("Tool Name", placeholder="e.g., get_stock_data")
            tool_override_vendor = st.selectbox(
                "Vendor",
                ["yfinance", "alpha_vantage", "openai", "google", "local"]
            )
            
            if st.button("Add Override"):
                if tool_override_key:
                    if "tool_vendors" not in st.session_state.config:
                        st.session_state.config["tool_vendors"] = {}
                    st.session_state.config["tool_vendors"][tool_override_key] = tool_override_vendor
                    st.success(f"Added override: {tool_override_key} -> {tool_override_vendor}")
            
            if st.session_state.config.get("tool_vendors"):
                st.markdown("**Current Overrides:**")
                for tool, vendor in st.session_state.config["tool_vendors"].items():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.text(f"{tool} → {vendor}")
                    with col_b:
                        if st.button("Remove", key=f"remove_{tool}"):
                            del st.session_state.config["tool_vendors"][tool]
                            st.rerun()
    
    with tab3:
        st.markdown("### Agent Parameters")
        st.markdown("Configure debate rounds, recursion limits, and other agent behaviors.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Discussion Parameters")
            
            max_debate_rounds = st.number_input(
                "Max Debate Rounds",
                min_value=1,
                max_value=10,
                value=st.session_state.config.get("max_debate_rounds", 1),
                help="Number of debate rounds between bull and bear researchers"
            )
            st.session_state.config["max_debate_rounds"] = max_debate_rounds
            
            max_risk_discuss_rounds = st.number_input(
                "Max Risk Discussion Rounds",
                min_value=1,
                max_value=10,
                value=st.session_state.config.get("max_risk_discuss_rounds", 1),
                help="Number of discussion rounds in risk management team"
            )
            st.session_state.config["max_risk_discuss_rounds"] = max_risk_discuss_rounds
        
        with col2:
            st.markdown("#### System Parameters")
            
            max_recur_limit = st.number_input(
                "Max Recursion Limit",
                min_value=10,
                max_value=500,
                value=st.session_state.config.get("max_recur_limit", 100),
                help="Maximum recursion depth for graph execution"
            )
            st.session_state.config["max_recur_limit"] = max_recur_limit
            
            results_dir = st.text_input(
                "Results Directory",
                value=st.session_state.config.get("results_dir", "./results"),
                help="Directory to store trading results"
            )
            st.session_state.config["results_dir"] = results_dir
        
        st.markdown("---")
        
        st.info("💡 **Performance Note**: Increasing debate rounds improves decision quality but increases API calls and execution time. Start with 1-2 rounds for testing.")
    
    with tab4:
        st.markdown("### API Keys Configuration")
        st.markdown("Configure your API keys for various services.")
        
        st.warning("⚠️ **Security Note**: API keys entered here are stored in session state and not persisted. For production use, always use environment variables or `.env` file.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### LLM Provider Keys")
            
            openai_key = st.text_input(
                "OpenAI API Key",
                value=os.getenv("OPENAI_API_KEY", ""),
                type="password",
                help="Your OpenAI API key"
            )
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
            
            anthropic_key = st.text_input(
                "Anthropic API Key",
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                type="password",
                help="Your Anthropic API key (for Claude)"
            )
            if anthropic_key:
                os.environ["ANTHROPIC_API_KEY"] = anthropic_key
            
            google_key = st.text_input(
                "Google API Key",
                value=os.getenv("GOOGLE_API_KEY", ""),
                type="password",
                help="Your Google API key (for Gemini)"
            )
            if google_key:
                os.environ["GOOGLE_API_KEY"] = google_key
        
        with col2:
            st.markdown("#### Data Provider Keys")
            
            alpha_vantage_key = st.text_input(
                "Alpha Vantage API Key",
                value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
                type="password",
                help="Your Alpha Vantage API key"
            )
            if alpha_vantage_key:
                os.environ["ALPHA_VANTAGE_API_KEY"] = alpha_vantage_key
            
            st.markdown("---")
            
            st.markdown("#### Get Free API Keys")
            st.markdown("- [OpenAI API](https://platform.openai.com/api-keys)")
            st.markdown("- [Alpha Vantage API](https://www.alphavantage.co/support/#api-key)")
            st.markdown("- [Anthropic API](https://console.anthropic.com/)")
            st.markdown("- [Google AI Studio](https://makersuite.google.com/app/apikey)")
    
    st.markdown("---")
    
    # Save/Export Configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Configuration", use_container_width=True):
            st.success("✓ Configuration saved to session!")
    
    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.session_state.config = DEFAULT_CONFIG.copy()
            st.success("✓ Configuration reset to defaults!")
            st.rerun()
    
    with col3:
        config_json = json.dumps(st.session_state.config, indent=2, default=str)
        st.download_button(
            "📥 Export Config JSON",
            data=config_json,
            file_name="tradingagents_config.json",
            mime="application/json",
            use_container_width=True
        )


def render_trading_execution() -> None:
    """Render trading execution page"""
    st.markdown('<div class="main-header">Trading Execution</div>', unsafe_allow_html=True)
    st.markdown("Execute trading analysis for a specific ticker and date.")
    
    # Configuration Summary
    with st.expander("📋 Current Configuration Summary"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("LLM Provider", st.session_state.config.get("llm_provider", "N/A"))
            st.metric("Deep Think LLM", st.session_state.config.get("deep_think_llm", "N/A"))
        with col2:
            st.metric("Quick Think LLM", st.session_state.config.get("quick_think_llm", "N/A"))
            st.metric("Debate Rounds", st.session_state.config.get("max_debate_rounds", "N/A"))
        with col3:
            st.metric("Core Stock API", st.session_state.config["data_vendors"].get("core_stock_apis", "N/A"))
            st.metric("News Source", st.session_state.config["data_vendors"].get("news_data", "N/A"))
    
    st.markdown("---")
    
    # Input Section
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        ticker = st.text_input(
            "Stock Ticker",
            value="NVDA",
            help="Enter the stock ticker symbol (e.g., NVDA, AAPL, TSLA)"
        ).upper()
    
    with col2:
        trade_date = st.date_input(
            "Trade Date",
            value=datetime.date(2024, 5, 10),
            help="Select the date for analysis"
        )
    
    with col3:
        st.markdown("##")
        debug_mode = st.checkbox("Debug Mode", value=False, help="Enable detailed logging")
    
    # Execution Button
    if st.button("🚀 Start Trading Analysis", use_container_width=True, type="primary"):
        if not ticker:
            st.error("Please enter a ticker symbol")
            return
        
        # Check API keys
        if not os.getenv("OPENAI_API_KEY") and st.session_state.config.get("llm_provider") == "openai":
            st.error("⚠️ OpenAI API key not found. Please configure it in the API Keys tab.")
            return
        
        # Create progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### 🔄 Execution Progress")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Agent status
            st.markdown("#### Agent Status")
            agent_status_container = st.container()
            
            # Results container
            results_container = st.empty()
            
            try:
                status_text.info(f"🔧 Initializing TradingAgents for {ticker} on {trade_date}...")
                progress_bar.progress(10)
                
                # Initialize TradingAgentsGraph
                ta = TradingAgentsGraph(
                    debug=debug_mode,
                    config=st.session_state.config
                )
                
                status_text.info("📊 Running analyst team...")
                progress_bar.progress(30)
                
                # Execute trading analysis
                final_state, decision = ta.propagate(ticker, str(trade_date))
                
                status_text.success("✅ Analysis complete!")
                progress_bar.progress(100)
                
                # Display results
                with results_container.container():
                    st.markdown("---")
                    st.markdown("### 📋 Trading Decision")
                    
                    # Decision box
                    decision_type = "HOLD"
                    if "BUY" in str(decision).upper():
                        decision_type = "BUY"
                        st.success(f"## 📈 BUY Signal")
                    elif "SELL" in str(decision).upper():
                        decision_type = "SELL"
                        st.error(f"## 📉 SELL Signal")
                    else:
                        st.warning(f"## ⏸️ HOLD Signal")
                    
                    st.markdown("#### Full Decision")
                    st.info(decision)
                    
                    # Detailed Reports
                    st.markdown("---")
                    st.markdown("### 📊 Detailed Analysis Reports")
                    
                    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                        "Market Analysis",
                        "Sentiment Analysis",
                        "News Analysis",
                        "Fundamentals",
                        "Research Debate",
                        "Risk Analysis"
                    ])
                    
                    with tab1:
                        if final_state.get("market_report"):
                            st.markdown(final_state["market_report"])
                        else:
                            st.info("No market analysis available")
                    
                    with tab2:
                        if final_state.get("sentiment_report"):
                            st.markdown(final_state["sentiment_report"])
                        else:
                            st.info("No sentiment analysis available")
                    
                    with tab3:
                        if final_state.get("news_report"):
                            st.markdown(final_state["news_report"])
                        else:
                            st.info("No news analysis available")
                    
                    with tab4:
                        if final_state.get("fundamentals_report"):
                            st.markdown(final_state["fundamentals_report"])
                        else:
                            st.info("No fundamentals analysis available")
                    
                    with tab5:
                        if final_state.get("investment_debate_state"):
                            debate = final_state["investment_debate_state"]
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**🐂 Bull Researcher**")
                                if debate.get("bull_history"):
                                    for msg in debate["bull_history"]:
                                        st.info(msg)
                            
                            with col2:
                                st.markdown("**🐻 Bear Researcher**")
                                if debate.get("bear_history"):
                                    for msg in debate["bear_history"]:
                                        st.warning(msg)
                            
                            st.markdown("**👨‍💼 Research Manager Decision**")
                            if debate.get("judge_decision"):
                                st.success(debate["judge_decision"])
                        else:
                            st.info("No research debate available")
                    
                    with tab6:
                        if final_state.get("risk_debate_state"):
                            risk = final_state["risk_debate_state"]
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown("**⚠️ Risky View**")
                                if risk.get("risky_history"):
                                    for msg in risk["risky_history"]:
                                        st.info(msg)
                            
                            with col2:
                                st.markdown("**⚖️ Neutral View**")
                                if risk.get("neutral_history"):
                                    for msg in risk["neutral_history"]:
                                        st.warning(msg)
                            
                            with col3:
                                st.markdown("**🛡️ Safe View**")
                                if risk.get("safe_history"):
                                    for msg in risk["safe_history"]:
                                        st.success(msg)
                            
                            st.markdown("**👔 Portfolio Manager Decision**")
                            if risk.get("judge_decision"):
                                st.success(risk["judge_decision"])
                        else:
                            st.info("No risk analysis available")
                    
                    # Export Results
                    st.markdown("---")
                    results_json = json.dumps(final_state, indent=2, default=str)
                    st.download_button(
                        "📥 Download Full Results (JSON)",
                        data=results_json,
                        file_name=f"trading_results_{ticker}_{trade_date}.json",
                        mime="application/json"
                    )
                
            except Exception as e:
                status_text.error(f"❌ Error during execution: {str(e)}")
                st.exception(e)
                progress_bar.progress(0)


def render_results_viewer() -> None:
    """Render results viewer page"""
    st.markdown('<div class="main-header">Results Viewer</div>', unsafe_allow_html=True)
    st.markdown("View and analyze historical trading results.")
    
    # Load results
    results = load_trading_results()
    
    if not results:
        st.info("📊 No trading results found. Execute some trades to see results here!")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        unique_tickers = ['All'] + sorted(df['ticker'].unique().tolist())
        selected_ticker = st.selectbox("Filter by Ticker", unique_tickers)
    
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(df['date'].min(), df['date'].max()),
            help="Select date range for filtering"
        )
    
    with col3:
        st.markdown("##")
        st.metric("Total Results", len(df))
    
    # Apply filters
    filtered_df = df.copy()
    if selected_ticker != 'All':
        filtered_df = filtered_df[filtered_df['ticker'] == selected_ticker]
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.Timestamp(date_range[0])) &
            (filtered_df['date'] <= pd.Timestamp(date_range[1]))
        ]
    
    # Display results table
    st.markdown("### Trading Results")
    st.dataframe(
        filtered_df[['ticker', 'date', 'decision']].sort_values('date', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Visualization
    if len(filtered_df) > 0:
        st.markdown("---")
        st.markdown("### Decision Distribution")
        
        # Count decisions
        decision_counts = {}
        for dec in filtered_df['decision']:
            dec_str = str(dec).upper()
            if 'BUY' in dec_str:
                decision_counts['BUY'] = decision_counts.get('BUY', 0) + 1
            elif 'SELL' in dec_str:
                decision_counts['SELL'] = decision_counts.get('SELL', 0) + 1
            else:
                decision_counts['HOLD'] = decision_counts.get('HOLD', 0) + 1
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(decision_counts.keys()),
            values=list(decision_counts.values()),
            hole=.3,
            marker=dict(colors=['#10b981', '#ef4444', '#f59e0b'])
        )])
        fig.update_layout(title="Trading Decisions Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline chart
        st.markdown("### Trading Timeline")
        timeline_df = filtered_df.groupby('date').size().reset_index(name='count')
        fig = px.line(timeline_df, x='date', y='count', markers=True)
        fig.update_layout(
            title="Number of Trades Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Trades"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed view
    st.markdown("---")
    st.markdown("### Detailed Result View")
    
    selected_result = st.selectbox(
        "Select a result to view details",
        filtered_df.apply(lambda x: f"{x['ticker']} - {x['date'].strftime('%Y-%m-%d')}", axis=1).tolist()
    )
    
    if selected_result:
        # Find the selected result
        ticker, date_str = selected_result.split(' - ')
        result_row = filtered_df[(filtered_df['ticker'] == ticker) & 
                                 (filtered_df['date'] == pd.Timestamp(date_str))].iloc[0]
        
        # Load and display full result
        try:
            with open(result_row['file'], 'r') as f:
                full_data = json.load(f)
                
                # Display in JSON viewer
                with st.expander("📄 View Full JSON"):
                    st.json(full_data)
                
                # Download button
                st.download_button(
                    "📥 Download This Result",
                    data=json.dumps(full_data, indent=2),
                    file_name=f"result_{ticker}_{date_str}.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"Error loading result details: {e}")


def render_about() -> None:
    """Render about page"""
    st.markdown('<div class="main-header">About TradingAgents</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Multi-Agent LLM Financial Trading Framework
    
    TradingAgents is a sophisticated multi-agent trading framework that mirrors the dynamics of real-world trading firms. 
    By deploying specialized LLM-powered agents, the platform collaboratively evaluates market conditions and informs trading decisions.
    
    ### 🎯 Key Features
    
    - **Multi-Agent Architecture**: Specialized agents for analysis, research, trading, and risk management
    - **Collaborative Decision Making**: Agents engage in structured debates to reach optimal strategies
    - **Flexible LLM Support**: Compatible with OpenAI, Anthropic, Google, and local models
    - **Configurable Data Sources**: Support for multiple data vendors (yfinance, Alpha Vantage, etc.)
    - **Research-Focused**: Designed for academic research and experimentation
    
    ### 👥 Agent Teams
    
    #### Analyst Team
    - **Fundamentals Analyst**: Evaluates company financials and performance metrics
    - **Sentiment Analyst**: Analyzes social media and public sentiment
    - **News Analyst**: Monitors global news and macroeconomic indicators
    - **Technical Analyst**: Utilizes technical indicators (MACD, RSI, etc.)
    
    #### Research Team
    - **Bull Researcher**: Optimistic perspective on market opportunities
    - **Bear Researcher**: Pessimistic perspective highlighting risks
    - **Research Manager**: Synthesizes debate and provides balanced view
    
    #### Trading Team
    - **Trader**: Executes trading decisions based on comprehensive research
    
    #### Risk Management Team
    - **Risk Analysts**: Evaluate risk from multiple perspectives
    - **Portfolio Manager**: Makes final approval/rejection decisions
    
    ### 📚 Citation
    
    If you use TradingAgents in your research, please cite:
    
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
    
    ### ⚠️ Disclaimer
    
    TradingAgents framework is designed for **research purposes only**. Trading performance may vary based on many factors, 
    including the chosen backbone language models, model temperature, trading periods, the quality of data, and other 
    non-deterministic factors. **It is not intended as financial, investment, or trading advice.**
    
    ### 🔗 Links
    
    - [GitHub Repository](https://github.com/TauricResearch/TradingAgents)
    - [arXiv Paper](https://arxiv.org/abs/2412.20138)
    - [Discord Community](https://discord.com/invite/hk9PGKShPK)
    - [Tauric Research](https://tauric.ai/)
    
    ### 📄 License
    
    This project is open source and available under the MIT License.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: October 2024
    """)


def main() -> None:
    """Main application entry point"""
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "⚙️ LLM Configuration":
        render_llm_config()
    elif page == "🚀 Trading Execution":
        render_trading_execution()
    elif page == "📊 Results Viewer":
        render_results_viewer()
    elif page == "ℹ️ About":
        render_about()


if __name__ == "__main__":
    main()
