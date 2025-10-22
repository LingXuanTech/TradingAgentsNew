#!/usr/bin/env python
"""
TradingAgents Installation Check Script
Verifies that all required components are properly installed and configured.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'plotly': 'plotly',
        'pandas': 'pandas',
        'langchain_openai': 'langchain-openai',
        'langgraph': 'langgraph',
        'yfinance': 'yfinance',
        'dotenv': 'python-dotenv',
        'rich': 'rich',
        'typer': 'typer',
        'questionary': 'questionary',
    }
    
    all_installed = True
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (not installed)")
            all_installed = False
    
    return all_installed

def check_api_keys():
    """Check if required API keys are configured"""
    print("\n🔍 Checking API keys...")
    
    # Load .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    api_keys = {
        'OPENAI_API_KEY': 'Required for LLM operations',
        'ALPHA_VANTAGE_API_KEY': 'Optional but recommended for market data',
        'ANTHROPIC_API_KEY': 'Optional (for Claude models)',
        'GOOGLE_API_KEY': 'Optional (for Gemini models)',
    }
    
    for key, description in api_keys.items():
        value = os.getenv(key)
        if value:
            masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            print(f"   ✅ {key}: {masked}")
        else:
            status = "⚠️ " if key == 'OPENAI_API_KEY' else "ℹ️ "
            print(f"   {status} {key}: Not set ({description})")

def check_project_structure():
    """Check if project structure is correct"""
    print("\n🔍 Checking project structure...")
    
    required_paths = [
        'tradingagents/',
        'tradingagents/graph/',
        'tradingagents/agents/',
        'tradingagents/dataflows/',
        'cli/',
        'web_app.py',
        'main.py',
        'requirements.txt',
        '.env.example',
    ]
    
    all_present = True
    for path in required_paths:
        full_path = Path(path)
        if full_path.exists():
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path} (missing)")
            all_present = False
    
    return all_present

def check_imports():
    """Check if core modules can be imported"""
    print("\n🔍 Checking core module imports...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        print("   ✅ TradingAgentsGraph")
        
        from tradingagents.default_config import DEFAULT_CONFIG
        print("   ✅ DEFAULT_CONFIG")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def check_directories():
    """Check and create necessary directories"""
    print("\n🔍 Checking/creating necessary directories...")
    
    directories = [
        'eval_results/',
        'results/',
        'tradingagents/dataflows/data_cache/',
    ]
    
    for dir_path in directories:
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ Created {dir_path}")
            except Exception as e:
                print(f"   ❌ Failed to create {dir_path}: {e}")
        else:
            print(f"   ✅ {dir_path} exists")

def run_quick_test():
    """Run a quick import test"""
    print("\n🔍 Running quick functionality test...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Just verify initialization works (don't run actual trading)
        config = DEFAULT_CONFIG.copy()
        print("   ✅ Configuration loaded successfully")
        print(f"   ℹ️  LLM Provider: {config.get('llm_provider', 'N/A')}")
        print(f"   ℹ️  Deep Think LLM: {config.get('deep_think_llm', 'N/A')}")
        print(f"   ℹ️  Quick Think LLM: {config.get('quick_think_llm', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("TradingAgents Installation Check")
    print("=" * 60)
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Structure': check_project_structure(),
        'Core Imports': check_imports(),
    }
    
    # Non-critical checks
    check_api_keys()
    check_directories()
    run_quick_test()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n✅ All critical checks passed!")
        print("\n🚀 You can now run the application:")
        print("   • CLI: python -m cli.main")
        print("   • Web: streamlit run web_app.py")
        print("   • Script: python main.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
