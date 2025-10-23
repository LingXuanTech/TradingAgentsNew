#!/bin/bash

# TradingAgents Web Dashboard Startup Script

echo "🚀 Starting TradingAgents Web Dashboard..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if requirements are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env with your API keys"
    fi
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ] && ! grep -q "OPENAI_API_KEY=" .env 2>/dev/null; then
    echo ""
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment or .env file"
    echo "   You can set it in the web interface or add it to .env"
    echo ""
fi

# Start the web app
echo "✅ Starting web dashboard at http://localhost:8501"
echo ""
streamlit run web_app.py
