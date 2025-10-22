"""
TradingAgents Streamlit现代化前端应用
使用shadcn/ui组件构建专业级的交易界面
"""

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# 设置页面配置
st.set_page_config(
    page_title="TradingAgents - 智能交易平台",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.tradingagents.ai',
        'Report a bug': 'https://github.com/TauricResearch/TradingAgents/issues',
        'About': 'TradingAgents v2.0 - 多智能体LLM交易系统'
    }
)

# 导入后端服务（这里需要根据实际的后端API调整）
# from ..api.client import TradingAPIClient

# 初始化会话状态
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = {
        'total_value': 100000.0,
        'daily_pnl': 2500.0,
        'positions': [],
        'trades': [],
        'alerts': []
    }

if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        'AAPL': {'price': 150.0, 'change': 2.5, 'volume': 1000000},
        'GOOGL': {'price': 2500.0, 'change': -15.0, 'volume': 500000},
        'MSFT': {'price': 300.0, 'change': 5.0, 'volume': 800000}
    }

# 侧边栏导航
def create_sidebar():
    """创建侧边栏导航"""
    with st.sidebar:
        ui.element("div", children=["TradingAgents"], className="text-2xl font-bold text-center mb-4")

        # 导航菜单
        pages = {
            "🏠 首页概览": "home",
            "📊 交易看板": "dashboard",
            "💹 交易管理": "trading",
            "🛡️ 风险控制": "risk",
            "📈 技术分析": "analysis",
            "⚙️ 系统设置": "settings"
        }

        selected_page = st.radio(
            "导航菜单",
            options=list(pages.keys()),
            index=0,
            label_visibility="collapsed"
        )

        st.divider()

        # 系统状态
        with ui.card(key="system_status"):
            ui.element("h4", children=["系统状态"], className="text-lg font-semibold mb-3")

            # 模拟状态数据
            status_items = [
                ("交易引擎", "运行中", "success"),
                ("市场监控", "运行中", "success"),
                ("风险控制", "启用", "info"),
                ("LLM服务", "正常", "success")
            ]

            for item, status, status_type in status_items:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{item}**")
                with col2:
                    if status_type == "success":
                        ui.element("span", children=[f"✅ {status}"], className="text-green-600")
                    elif status_type == "warning":
                        ui.element("span", children=[f"⚠️ {status}"], className="text-yellow-600")
                    else:
                        ui.element("span", children=[f"ℹ️ {status}"], className="text-blue-600")

        # 快速操作
        st.divider()
        ui.element("h4", children=["快速操作"], className="text-lg font-semibold mb-3")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 启动交易", use_container_width=True):
                st.success("交易系统已启动")
        with col2:
            if st.button("⏹️ 停止交易", use_container_width=True):
                st.warning("交易系统已停止")

        if st.button("📊 生成报告", use_container_width=True):
            st.info("报告生成中...")

        if st.button("🔄 刷新数据", use_container_width=True):
            st.rerun()

def create_home_page():
    """首页概览页面"""
    st.title("🚀 TradingAgents 智能交易平台")

    # 顶部指标卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="总资产价值",
            content=f"¥{st.session_state.portfolio_data['total_value']:,.",.2f"
            description=f"+¥{st.session_state.portfolio_data['daily_pnl']:,.2f"}今日",
            key="portfolio_metric"
        )

    with col2:
        ui.metric_card(
            title="持仓股票",
            content=f"{len(st.session_state.portfolio_data['positions'])}只",
            description="实时持仓数量",
            key="positions_metric"
        )

    with col3:
        ui.metric_card(
            title="今日交易",
            content="12笔",
            description="胜率 75%",
            key="trades_metric"
        )

    with col4:
        ui.metric_card(
            title="风险等级",
            content="低风险",
            description="安全系数 95%",
            key="risk_metric"
        )

    st.divider()

    # 主要内容区域
    tab1, tab2, tab3 = st.tabs(["📊 投资组合", "📈 市场概览", "🔔 最新动态"])

    with tab1:
        create_portfolio_overview()

    with tab2:
        create_market_overview()

    with tab3:
        create_recent_activity()

def create_portfolio_overview():
    """投资组合概览"""
    st.subheader("投资组合详情")

    # 持仓表格
    if st.session_state.portfolio_data['positions']:
        positions_df = pd.DataFrame(st.session_state.portfolio_data['positions'])

        # 使用streamlit-shadcn-ui的数据表格组件
        ui.dataframe(
            positions_df,
            use_container_width=True,
            key="positions_table"
        )
    else:
        st.info("暂无持仓数据")

    # 资产分配饼图
    st.subheader("资产分配")

    if st.session_state.portfolio_data['positions']:
        # 创建饼图数据
        pie_data = positions_df[['symbol', 'market_value']].copy()
        pie_data.columns = ['股票', '市值']

        fig = px.pie(
            pie_data,
            values='市值',
            names='股票',
            title='持仓市值分布',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无资产分配数据")

def create_market_overview():
    """市场概览"""
    st.subheader("实时市场数据")

    # 市场数据表格
    market_df = pd.DataFrame([
        {'股票': symbol, **data}
        for symbol, data in st.session_state.market_data.items()
    ])

    ui.dataframe(
        market_df,
        use_container_width=True,
        key="market_table"
    )

    # 价格趋势图（模拟数据）
    st.subheader("价格趋势")

    # 生成模拟的价格数据
    dates = pd.date_range(datetime.now() - timedelta(days=7), datetime.now(), freq='H')
    trend_data = []

    for symbol in st.session_state.market_data.keys():
        base_price = st.session_state.market_data[symbol]['price']
        for date in dates:
            # 添加随机波动
            price = base_price + np.random.normal(0, base_price * 0.02)
            trend_data.append({
                '时间': date,
                '股票': symbol,
                '价格': max(0, price)
            })

    trend_df = pd.DataFrame(trend_data)

    # 创建价格趋势图
    fig = px.line(
        trend_df,
        x='时间',
        y='价格',
        color='股票',
        title='7天价格趋势',
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

def create_recent_activity():
    """最新动态"""
    st.subheader("交易活动和预警")

    # 模拟交易记录
    activities = [
        {"时间": "14:30:25", "类型": "交易", "描述": "AAPL 买入 100股 @ ¥150.00", "状态": "success"},
        {"时间": "14:25:10", "类型": "预警", "描述": "持仓风险等级升高", "状态": "warning"},
        {"时间": "14:20:05", "类型": "分析", "描述": "技术指标发出买入信号", "状态": "info"},
        {"时间": "14:15:30", "类型": "交易", "描述": "GOOGL 卖出 50股 @ ¥2500.00", "状态": "success"},
    ]

    for activity in activities:
        if activity["状态"] == "success":
            ui.element("div", children=[
                ui.element("span", children=[f"✅ {activity['时间']}"], className="text-green-600 font-mono text-sm"),
                ui.element("span", children=[activity["类型"]], className="mx-2 px-2 py-1 bg-green-100 text-green-800 rounded text-xs"),
                activity["描述"]
            ], className="mb-2 p-2 border-l-4 border-green-500 bg-gray-50")
        elif activity["状态"] == "warning":
            ui.element("div", children=[
                ui.element("span", children=[f"⚠️ {activity['时间']}"], className="text-yellow-600 font-mono text-sm"),
                ui.element("span", children=[activity["类型"]], className="mx-2 px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs"),
                activity["描述"]
            ], className="mb-2 p-2 border-l-4 border-yellow-500 bg-gray-50")
        else:
            ui.element("div", children=[
                ui.element("span", children=[f"ℹ️ {activity['时间']}"], className="text-blue-600 font-mono text-sm"),
                ui.element("span", children=[activity["类型"]], className="mx-2 px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"),
                activity["描述"]
            ], className="mb-2 p-2 border-l-4 border-blue-500 bg-gray-50")

def create_dashboard_page():
    """交易看板页面"""
    st.title("📊 交易看板")

    # 实时指标
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="总资产",
            content=f"¥{st.session_state.portfolio_data['total_value']:,.2f}",
            description="实时价值",
            key="total_assets"
        )

    with col2:
        daily_pnl = st.session_state.portfolio_data['daily_pnl']
        pnl_color = "green" if daily_pnl >= 0 else "red"
        ui.metric_card(
            title="今日盈亏",
            content=f"{daily_pnl:+,.2f}",
            description="较昨日",
            key="daily_pnl"
        )

    with col3:
        ui.metric_card(
            title="持仓数量",
            content=f"{len(st.session_state.portfolio_data['positions'])}只",
            description="股票持仓",
            key="holdings_count"
        )

    with col4:
        ui.metric_card(
            title="风险等级",
            content="低风险",
            description="安全系数 95%",
            key="risk_level"
        )

    st.divider()

    # 主要内容区
    tab1, tab2, tab3 = st.tabs(["📊 持仓详情", "📈 图表分析", "🔔 交易记录"])

    with tab1:
        create_positions_detail()

    with tab2:
        create_charts_analysis()

    with tab3:
        create_trades_history()

def create_positions_detail():
    """持仓详情"""
    st.subheader("当前持仓")

    positions = st.session_state.portfolio_data['positions']

    if not positions:
        st.info("暂无持仓数据")
        return

    # 创建持仓数据表格
    positions_df = pd.DataFrame(positions)

    # 使用shadcn/ui风格的数据表格
    with ui.card(key="positions_card"):
        ui.dataframe(
            positions_df,
            use_container_width=True,
            key="positions_detail_table"
        )

    # 操作按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 刷新数据", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📤 导出Excel", use_container_width=True):
            st.success("持仓数据已导出")
    with col3:
        if st.button("⚡ 一键调仓", use_container_width=True):
            st.info("智能调仓建议生成中...")

def create_charts_analysis():
    """图表分析"""
    st.subheader("投资组合分析")

    # 资产分配饼图
    st.subheader("资产分配构成")

    positions = st.session_state.portfolio_data['positions']
    if positions:
        # 准备饼图数据
        pie_data = []
        for pos in positions:
            pie_data.append({
                '股票': pos['symbol'],
                '市值': pos['market_value'],
                '比例': pos['market_value'] / sum(p['market_value'] for p in positions) * 100
            })

        pie_df = pd.DataFrame(pie_data)

        fig_pie = px.pie(
            pie_df,
            values='市值',
            names='股票',
            title='持仓市值分布',
            hover_data=['比例'],
            labels={'比例': '占比 (%)'}
        )

        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("暂无持仓数据，无法生成图表")

    # 盈亏趋势图（模拟数据）
    st.subheader("盈亏趋势分析")

    # 生成模拟的历史数据
    dates = pd.date_range(datetime.now() - timedelta(days=30), datetime.now(), freq='D')
    pnl_history = []

    base_pnl = 100000
    for i, date in enumerate(dates):
        # 模拟每日盈亏波动
        daily_change = np.random.normal(0, 1000)
        base_pnl += daily_change
        pnl_history.append({
            '日期': date.strftime('%m-%d'),
            '累计盈亏': base_pnl,
            '每日盈亏': daily_change
        })

    pnl_df = pd.DataFrame(pnl_history)

    fig_line = px.line(
        pnl_df,
        x='日期',
        y='累计盈亏',
        title='30天盈亏趋势',
        markers=True
    )

    st.plotly_chart(fig_line, use_container_width=True)

def create_trades_history():
    """交易历史记录"""
    st.subheader("交易历史记录")

    # 筛选控件
    col1, col2, col3 = st.columns(3)

    with col1:
        symbol_filter = st.selectbox(
            "股票筛选",
            ["全部", "AAPL", "GOOGL", "MSFT"],
            key="trades_symbol_filter"
        )

    with col2:
        time_filter = st.selectbox(
            "时间筛选",
            ["今日", "本周", "本月", "全部"],
            key="trades_time_filter"
        )

    with col3:
        status_filter = st.selectbox(
            "状态筛选",
            ["全部", "已成交", "待成交", "已取消"],
            key="trades_status_filter"
        )

    # 模拟交易数据
    trades_data = []
    for i in range(20):
        trade_date = datetime.now() - timedelta(hours=i*2)
        trades_data.append({
            "交易时间": trade_date.strftime('%m-%d %H:%M'),
            "股票代码": np.random.choice(['AAPL', 'GOOGL', 'MSFT']),
            "交易方向": np.random.choice(['买入', '卖出']),
            "数量": np.random.randint(10, 1000),
            "价格": round(np.random.uniform(100, 300), 2),
            "金额": 0,  # 计算得出
            "手续费": round(np.random.uniform(5, 50), 2),
            "盈亏": round(np.random.uniform(-500, 1000), 2),
            "状态": np.random.choice(['已成交', '待成交', '已取消'])
        })

    # 计算金额
    for trade in trades_data:
        trade['金额'] = trade['数量'] * trade['价格']

    trades_df = pd.DataFrame(trades_data)

    # 应用筛选
    if symbol_filter != "全部":
        trades_df = trades_df[trades_df['股票代码'] == symbol_filter]

    if status_filter != "全部":
        trades_df = trades_df[trades_df['状态'] == status_filter]

    # 显示交易记录
    with ui.card(key="trades_card"):
        ui.dataframe(
            trades_df,
            use_container_width=True,
            key="trades_history_table"
        )

    # 分页和统计
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("总交易笔数", len(trades_df))

    with col2:
        profitable_trades = len(trades_df[trades_df['盈亏'] > 0])
        win_rate = (profitable_trades / len(trades_df) * 100) if len(trades_df) > 0 else 0
        st.metric("胜率", f"{win_rate:.1f}%")

    with col3:
        total_pnl = trades_df['盈亏'].sum()
        st.metric("总盈亏", f"¥{total_pnl:,.2f}")

def create_trading_page():
    """交易管理页面"""
    st.title("💹 交易管理")

    tab1, tab2 = st.tabs(["🚀 快速交易", "📋 订单管理"])

    with tab1:
        create_quick_trading()

    with tab2:
        create_order_management()

def create_quick_trading():
    """快速交易界面"""
    st.subheader("快速下单")

    col1, col2 = st.columns([2, 1])

    with col1:
        with ui.card(key="trading_form"):
            ui.element("h4", children=["交易订单"], className="mb-4")

            # 交易表单
            trade_symbol = st.selectbox(
                "选择股票",
                ["AAPL", "GOOGL", "MSFT", "000858.SZ", "600519.SS"],
                key="trade_symbol"
            )

            col_a, col_b = st.columns(2)
            with col_a:
                trade_side = st.radio(
                    "交易方向",
                    ["买入", "卖出"],
                    horizontal=True,
                    key="trade_side"
                )

            with col_b:
                order_type = st.selectbox(
                    "订单类型",
                    ["市价单", "限价单", "止损单"],
                    key="order_type"
                )

            quantity = st.number_input(
                "交易数量",
                min_value=1,
                value=100,
                step=100,
                key="trade_quantity"
            )

            # 根据订单类型显示价格输入
            trade_price = None
            if order_type in ["限价单", "止损单"]:
                trade_price = st.number_input(
                    "订单价格",
                    min_value=0.01,
                    value=st.session_state.market_data.get(trade_symbol, {}).get('price', 100.0),
                    step=0.01,
                    key="trade_price"
                )

            # 交易按钮
            if st.button("🚀 立即下单", type="primary", use_container_width=True):
                # 模拟下单逻辑
                st.success(f"订单提交成功：{trade_side} {quantity}股 {trade_symbol}")

                # 显示订单详情
                with st.expander("订单详情", expanded=True):
                    st.json({
                        "symbol": trade_symbol,
                        "side": trade_side,
                        "quantity": quantity,
                        "order_type": order_type,
                        "price": trade_price,
                        "timestamp": datetime.now().isoformat(),
                        "status": "pending"
                    })

    with col2:
        # 市场行情
        with ui.card(key="market_quotes"):
            ui.element("h5", children=["市场行情"], className="mb-3")

            for symbol, data in st.session_state.market_data.items():
                pnl_class = "success" if data['change'] >= 0 else "danger"

                with st.container():
                    st.write(f"**{symbol}**")
                    st.write(f"价格: ¥{data['price']}")
                    st.write(f"涨跌: {data['change']:+.2f}")
                    st.write(f"成交量: {data['volume']:,}", ",.0f")
                    st.divider()

def create_order_management():
    """订单管理"""
    st.subheader("订单管理")

    # 订单状态标签页
    tab1, tab2, tab3 = st.tabs(["📋 全部订单", "⏳ 待成交", "✅ 已成交"])

    for tab, status_filter in [(tab1, "全部"), (tab2, "待成交"), (tab3, "已成交")]:
        with tab:
            # 模拟订单数据
            orders_data = []
            for i in range(10):
                orders_data.append({
                    "订单号": f"ORD{datetime.now().strftime('%Y%m%d')}{i+1:03d}",
                    "股票代码": np.random.choice(['AAPL', 'GOOGL', 'MSFT']),
                    "交易方向": np.random.choice(['买入', '卖出']),
                    "订单类型": np.random.choice(['市价单', '限价单']),
                    "数量": np.random.randint(10, 1000),
                    "价格": round(np.random.uniform(100, 300), 2),
                    "状态": np.random.choice(['待成交', '已成交', '已取消']),
                    "下单时间": (datetime.now() - timedelta(minutes=i*5)).strftime('%H:%M:%S')
                })

            orders_df = pd.DataFrame(orders_data)

            if status_filter != "全部":
                status_map = {"待成交": "待成交", "已成交": "已成交"}
                orders_df = orders_df[orders_df['状态'] == status_map.get(status_filter, status_filter)]

            if not orders_df.empty:
                ui.dataframe(
                    orders_df,
                    use_container_width=True,
                    key=f"orders_table_{status_filter}"
                )

                # 批量操作
                if status_filter == "待成交":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("批量撤单", key=f"cancel_all_{status_filter}"):
                            st.warning("已提交批量撤单请求")
                    with col2:
                        if st.button("全部成交", key=f"fill_all_{status_filter}"):
                            st.success("已提交全部成交请求")
            else:
                st.info(f"暂无{status_filter}订单")

def create_risk_page():
    """风险控制页面"""
    st.title("🛡️ 风险控制中心")

    # 风险指标概览
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="持仓风险",
            content="15.2%",
            description="低于警戒线 25%",
            key="position_risk"
        )

    with col2:
        ui.metric_card(
            title="资金利用率",
            content="68.5%",
            description="现金余额充足",
            key="capital_usage"
        )

    with col3:
        ui.metric_card(
            title="最大回撤",
            content="-3.2%",
            description="控制在合理范围",
            key="max_drawdown"
        )

    with col4:
        ui.metric_card(
            title="风险评级",
            content="A级",
            description="低风险等级",
            key="risk_rating"
        )

    st.divider()

    # 风险控制面板
    tab1, tab2, tab3 = st.tabs(["⚙️ 风控设置", "📊 风险分析", "🚨 风险预警"])

    with tab1:
        create_risk_settings()

    with tab2:
        create_risk_analysis()

    with tab3:
        create_risk_alerts()

def create_risk_settings():
    """风险控制设置"""
    st.subheader("风险控制参数设置")

    with ui.card(key="risk_settings"):
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "单股最大持仓比例 (%)",
                min_value=1.0,
                max_value=50.0,
                value=20.0,
                step=1.0,
                key="max_position_ratio"
            )

            st.number_input(
                "投资组合最大风险 (%)",
                min_value=5.0,
                max_value=100.0,
                value=25.0,
                step=5.0,
                key="max_portfolio_risk"
            )

            st.number_input(
                "单日最大亏损比例 (%)",
                min_value=1.0,
                max_value=20.0,
                value=5.0,
                step=1.0,
                key="max_daily_loss"
            )

        with col2:
            st.number_input(
                "止损比例 (%)",
                min_value=1.0,
                max_value=30.0,
                value=8.0,
                step=1.0,
                key="stop_loss_ratio"
            )

            st.number_input(
                "止盈比例 (%)",
                min_value=5.0,
                max_value=100.0,
                value=25.0,
                step=5.0,
                key="take_profit_ratio"
            )

            st.number_input(
                "单日最大订单数",
                min_value=1,
                max_value=100,
                value=20,
                step=5,
                key="max_orders_per_day"
            )

        # 高级设置
        with st.expander("高级风险控制设置"):
            st.checkbox("启用动态止损", value=True, key="enable_dynamic_stop")
            st.checkbox("启用追踪止损", value=False, key="enable_trailing_stop")
            st.checkbox("启用风险平仓", value=True, key="enable_force_close")

        # 保存设置
        if st.button("💾 保存风控设置", type="primary", use_container_width=True):
            st.success("风控设置已保存")

def create_risk_analysis():
    """风险分析"""
    st.subheader("风险分析报告")

    # 风险构成分析
    st.subheader("风险构成分解")

    # 模拟风险数据
    risk_data = {
        '市场风险': 45,
        '流动性风险': 25,
        '集中度风险': 20,
        '杠杆风险': 10
    }

    # 风险构成饼图
    risk_df = pd.DataFrame(list(risk_data.items()), columns=['风险类型', '占比'])

    fig_risk = px.pie(
        risk_df,
        values='占比',
        names='风险类型',
        title='风险构成分析',
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    st.plotly_chart(fig_risk, use_container_width=True)

    # 风险指标详情
    st.subheader("详细风险指标")

    risk_metrics = [
        {"指标": "Beta系数", "当前值": 0.85, "参考值": "< 1.0", "状态": "正常"},
        {"指标": "夏普比率", "当前值": 1.25, "参考值": "> 1.0", "状态": "良好"},
        {"指标": "最大回撤", "当前值": -3.2, "参考值": "< -5%", "状态": "正常"},
        {"指标": "VaR (95%)", "当前值": -1.8, "参考值": "< -2%", "状态": "正常"},
        {"指标": "持仓集中度", "当前值": 15.2, "参考值": "< 20%", "状态": "正常"}
    ]

    for metric in risk_metrics:
        status_class = "success" if metric["状态"] == "良好" else "normal"
        st.metric(
            label=f"{metric['指标']} ({metric['参考值']})",
            value=f"{metric['当前值']}",
            delta=metric["状态"],
            delta_color="normal" if metric["状态"] == "正常" else "normal"
        )

def create_risk_alerts():
    """风险预警"""
    st.subheader("风险预警信息")

    # 模拟预警数据
    alerts = [
        {
            "时间": "14:30:25",
            "等级": "低",
            "类型": "持仓比例预警",
            "描述": "AAPL持仓比例接近20%上限",
            "建议": "考虑减仓或分散投资"
        },
        {
            "时间": "14:25:10",
            "等级": "中",
            "类型": "市场波动预警",
            "描述": "市场波动率升高10%",
            "建议": "谨慎交易，关注止损设置"
        },
        {
            "时间": "14:20:05",
            "等级": "低",
            "类型": "资金利用率预警",
            "描述": "现金利用率偏低",
            "建议": "可适当增加投资仓位"
        }
    ]

    for alert in alerts:
        if alert["等级"] == "高":
            alert_class = "danger"
            icon = "🔴"
        elif alert["等级"] == "中":
            alert_class = "warning"
            icon = "🟡"
        else:
            alert_class = "info"
            icon = "🔵"

        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{icon} {alert['等级']}级预警**")
                st.caption(alert["时间"])
            with col2:
                st.write(f"**{alert['类型']}**")
                st.write(alert["描述"])
                st.info(f"💡 建议：{alert['建议']}")
            st.divider()

def create_analysis_page():
    """技术分析页面"""
    st.title("📈 技术分析中心")

    # 分析工具选择
    analysis_tools = st.multiselect(
        "选择技术指标",
        [
            "移动平均线", "MACD", "RSI", "布林带",
            "KDJ随机指标", "威廉指标", "CCI顺势指标",
            "成交量分析", "支撑阻力位", "形态识别"
        ],
        default=["移动平均线", "MACD", "RSI"],
        key="analysis_tools"
    )

    st.divider()

    # 股票选择和时间周期
    col1, col2, col3 = st.columns(3)

    with col1:
        analysis_symbol = st.selectbox(
            "分析股票",
            ["AAPL", "GOOGL", "MSFT", "000858.SZ", "600519.SS"],
            key="analysis_symbol"
        )

    with col2:
        time_period = st.selectbox(
            "时间周期",
            ["1分钟", "5分钟", "15分钟", "30分钟", "1小时", "日K", "周K"],
            key="time_period"
        )

    with col3:
        analysis_period = st.selectbox(
            "分析周期",
            ["最近7天", "最近30天", "最近90天", "最近1年"],
            key="analysis_period"
        )

    # 生成技术分析报告
    if st.button("🔍 生成技术分析报告", type="primary", use_container_width=True):
        with st.status("正在生成技术分析报告...", expanded=True) as status:
            st.write("📊 收集市场数据...")
            time.sleep(1)

            st.write("📈 计算技术指标...")
            time.sleep(1)

            st.write("🔍 识别交易信号...")
            time.sleep(1)

            status.update(label="✅ 分析完成！", state="complete")

        # 显示分析结果
        show_technical_analysis(analysis_symbol, analysis_tools)

def show_technical_analysis(symbol, tools):
    """显示技术分析结果"""
    st.subheader(f"{symbol} 技术分析报告")

    # 模拟技术分析结果
    analysis_results = {}

    if "移动平均线" in tools:
        analysis_results["移动平均线"] = {
            "ma5": 150.25,
            "ma10": 149.80,
            "ma20": 148.50,
            "趋势": "上升"
        }

    if "MACD" in tools:
        analysis_results["MACD"] = {
            "macd": 1.25,
            "signal": 1.10,
            "histogram": 0.15,
            "信号": "买入"
        }

    if "RSI" in tools:
        analysis_results["RSI"] = {
            "rsi": 65.5,
            "状态": "适中",
            "信号": "持有"
        }

    # 显示分析结果
    cols = st.columns(len(analysis_results))
    for i, (tool_name, result) in enumerate(analysis_results.items()):
        with cols[i]:
            with ui.card(key=f"analysis_{tool_name}_{i}"):
                ui.element("h6", children=[tool_name], className="mb-3")
                for key, value in result.items():
                    st.write(f"**{key}:** {value}")

def create_settings_page():
    """系统设置页面"""
    st.title("⚙️ 系统设置")

    tab1, tab2, tab3, tab4 = st.tabs(["🔧 基础设置", "🤖 LLM配置", "📊 数据源", "🔒 安全设置"])

    with tab1:
        create_basic_settings()

    with tab2:
        create_llm_settings()

    with tab3:
        create_data_source_settings()

    with tab4:
        create_security_settings()

def create_basic_settings():
    """基础设置"""
    st.subheader("基础配置")

    with ui.card(key="basic_settings"):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("系统名称", value="TradingAgents", key="system_name")
            st.selectbox(
                "运行环境",
                ["development", "testing", "production"],
                key="environment"
            )
            st.selectbox(
                "日志级别",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                key="log_level"
            )

        with col2:
            auto_start = st.checkbox("开机自启动", value=True, key="auto_start")
            enable_notifications = st.checkbox("启用通知", value=True, key="enable_notifications")
            enable_backup = st.checkbox("自动备份", value=True, key="enable_backup")

        if st.button("💾 保存基础设置", use_container_width=True):
            st.success("基础设置已保存")

def create_llm_settings():
    """LLM配置"""
    st.subheader("多智能体LLM配置")

    # LLM供应商选择
    st.subheader("LLM供应商设置")

    providers = {
        "研究员": {"model": "o1-preview", "provider": "openai"},
        "分析师": {"model": "gpt-4o", "provider": "openai"},
        "交易员": {"model": "gpt-4o", "provider": "openai"},
        "风险管理": {"model": "gpt-4o", "provider": "openai"}
    }

    for agent, config in providers.items():
        with st.expander(f"{agent} LLM配置"):
            col1, col2 = st.columns(2)
            with col1:
                provider = st.selectbox(
                    f"{agent}供应商",
                    ["OpenAI", "Anthropic", "Google"],
                    key=f"{agent}_provider"
                )
                model = st.selectbox(
                    f"{agent}模型",
                    ["gpt-4o", "gpt-4o-mini", "o1-preview", "claude-3-5-sonnet"],
                    key=f"{agent}_model"
                )

            with col2:
                temperature = st.slider(
                    f"{agent}创造性",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    step=0.1,
                    key=f"{agent}_temperature"
                )
                max_tokens = st.number_input(
                    f"{agent}最大token",
                    min_value=512,
                    max_value=8192,
                    value=2048,
                    key=f"{agent}_max_tokens"
                )

    if st.button("💾 保存LLM配置", use_container_width=True):
        st.success("LLM配置已保存")

def create_data_source_settings():
    """数据源设置"""
    st.subheader("数据源配置")

    with ui.card(key="data_sources"):
        # 数据供应商配置
        data_providers = {
            "股票数据": ["yfinance", "alpha_vantage", "本地数据"],
            "技术指标": ["yfinance", "alpha_vantage", "本地计算"],
            "基本面数据": ["alpha_vantage", "本地数据"],
            "新闻数据": ["alpha_vantage", "google_news", "本地数据"]
        }

        for data_type, providers in data_providers.items():
            st.selectbox(
                data_type,
                providers,
                key=f"data_provider_{data_type}"
            )

        st.divider()

        # 数据更新频率
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "实时数据更新间隔 (秒)",
                min_value=1,
                max_value=300,
                value=5,
                key="realtime_update_interval"
            )

        with col2:
            st.number_input(
                "历史数据缓存时间 (小时)",
                min_value=1,
                max_value=168,
                value=24,
                key="cache_duration"
            )

        if st.button("💾 保存数据源配置", use_container_width=True):
            st.success("数据源配置已保存")

def create_security_settings():
    """安全设置"""
    st.subheader("安全配置")

    with ui.card(key="security_settings"):
        # API密钥管理
        st.subheader("API密钥管理")

        api_keys = {
            "华泰证券": "ht_app_key",
            "广发证券": "gf_app_key",
            "OpenAI": "openai_key",
            "邮件服务": "email_key"
        }

        for name, key_id in api_keys.items():
            with st.expander(f"{name} API配置"):
                api_key = st.text_input(
                    f"{name} API密钥",
                    type="password",
                    key=f"api_key_{key_id}"
                )
                if st.button(f"验证{name}连接", key=f"test_{key_id}"):
                    st.success(f"{name}连接正常")

        st.divider()

        # 安全选项
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("启用两因素认证", key="enable_2fa")
            st.checkbox("启用操作审计日志", value=True, key="enable_audit_log")
            st.checkbox("启用敏感操作确认", value=True, key="enable_confirmations")

        with col2:
            st.checkbox("启用自动登出", key="enable_auto_logout")
            st.number_input(
                "会话超时时间 (分钟)",
                min_value=5,
                max_value=480,
                value=60,
                key="session_timeout"
            )

        if st.button("💾 保存安全配置", use_container_width=True):
            st.success("安全配置已保存")

# 主应用路由
def main():
    """主应用"""
    # 创建侧边栏
    create_sidebar()

    # 根据路由显示页面内容
    # 这里简化处理，实际应用中应该使用更复杂的路由系统
    page = st.query_params.get("page", "home")

    if page == "home" or page == "首页概览":
        create_home_page()
    elif page == "dashboard" or page == "交易看板":
        create_dashboard_page()
    elif page == "trading" or page == "交易管理":
        create_trading_page()
    elif page == "risk" or page == "风险控制":
        create_risk_page()
    elif page == "analysis" or page == "技术分析":
        create_analysis_page()
    elif page == "settings" or page == "系统设置":
        create_settings_page()
    else:
        create_home_page()

if __name__ == "__main__":
    main()