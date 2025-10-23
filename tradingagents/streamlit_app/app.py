"""
TradingAgents Streamlit应用启动器
提供现代化的Web界面，支持多页面导航和实时数据更新
"""

import streamlit as st
from main import main
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.streamlit_app.main import main

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
else:
    # 当通过streamlit run直接启动时也运行main
    main()