"""
TradingAgents Streamlit应用启动器
提供现代化的Web界面，支持多页面导航和实时数据更新
"""

import streamlit as st
from main import main

# 页面标题和图标
st.set_page_config(
    page_title="TradingAgents - 智能交易平台",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 启动主应用
if __name__ == "__main__":
    main()