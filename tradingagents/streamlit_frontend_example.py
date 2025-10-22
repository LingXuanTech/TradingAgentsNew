#!/usr/bin/env python3
"""
TradingAgents Streamlit前端使用示例
展示现代化Web界面的各项功能
"""

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# 设置页面配置
st.set_page_config(
    page_title="TradingAgents - 前端演示",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """主函数"""
    st.title("🚀 TradingAgents Streamlit前端演示")
    st.info("这是TradingAgents现代化前端的演示版本，展示shadcn/ui组件的使用效果")

    # 创建侧边栏
    with st.sidebar:
        st.title("🎛️ 控制面板")

        # 页面选择
        page = st.radio(
            "选择演示页面",
            ["首页概览", "交易看板", "技术分析", "风险控制", "系统设置"],
            key="demo_page"
        )

        st.divider()

        # 功能开关
        st.subheader("功能开关")
        enable_realtime = st.checkbox("启用实时更新", value=True, key="realtime_switch")
        enable_notifications = st.checkbox("启用通知", value=True, key="notification_switch")
        dark_mode = st.checkbox("深色主题", value=False, key="dark_mode_switch")

        st.divider()

        # 快速操作
        st.subheader("快速操作")
        if st.button("🔄 刷新数据", use_container_width=True):
            st.rerun()

        if st.button("📊 生成报告", use_container_width=True):
            st.success("演示报告已生成")

        if st.button("🚀 启动交易", use_container_width=True):
            st.success("交易系统已启动")

    # 根据选择显示不同页面
    if page == "首页概览":
        show_home_demo()
    elif page == "交易看板":
        show_dashboard_demo()
    elif page == "技术分析":
        show_analysis_demo()
    elif page == "风险控制":
        show_risk_demo()
    elif page == "系统设置":
        show_settings_demo()

def show_home_demo():
    """首页概览演示"""
    st.header("🏠 首页概览")

    # 使用shadcn/ui组件展示指标
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="总资产价值",
            content="¥1,025,000",
            description="+¥25,000 今日",
            key="demo_portfolio"
        )

    with col2:
        ui.metric_card(
            title="持仓股票",
            content="8只",
            description="分散投资组合",
            key="demo_positions"
        )

    with col3:
        ui.metric_card(
            title="今日交易",
            content="15笔",
            description="胜率 73%",
            key="demo_trades"
        )

    with col4:
        ui.metric_card(
            title="风险等级",
            content="中等",
            description="安全系数 85%",
            key="demo_risk"
        )

    st.divider()

    # 资产分配图表
    st.subheader("资产分配可视化")

    # 创建模拟数据
    assets_data = pd.DataFrame({
        '资产类型': ['股票', '现金', '债券', '基金'],
        '市值': [600000, 300000, 100000, 25000],
        '占比': [60, 30, 10, 2.5]
    })

    fig = px.pie(
        assets_data,
        values='市值',
        names='资产类型',
        title='投资组合构成',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig, use_container_width=True)

    # 近期交易活动
    st.subheader("近期交易活动")

    # 使用shadcn/ui创建活动时间线
    activities = [
        {"时间": "14:30", "类型": "买入", "股票": "AAPL", "数量": 100, "价格": 150.0},
        {"时间": "14:25", "类型": "卖出", "股票": "GOOGL", "数量": 50, "价格": 2500.0},
        {"时间": "14:20", "类型": "买入", "股票": "MSFT", "数量": 200, "价格": 300.0},
    ]

    for activity in activities:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.write(f"**{activity['时间']}**")

            with col2:
                type_color = "🟢" if activity['类型'] == "买入" else "🔴"
                st.write(f"{type_color} {activity['类型']} {activity['股票']} {activity['数量']}股")

            with col3:
                st.write(f"¥{activity['价格']:.2f}")

            st.divider()

def show_dashboard_demo():
    """交易看板演示"""
    st.header("📊 交易看板演示")

    # 实时指标
    st.subheader("实时指标")

    # 使用shadcn/ui的metric_card
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui.metric_card(
            title="总资产",
            content="¥1,025,000",
            description="实时价值",
            key="live_portfolio"
        )

    with col2:
        ui.metric_card(
            title="今日盈亏",
            content="+¥25,000",
            description="较昨日",
            key="live_pnl"
        )

    with col3:
        ui.metric_card(
            title="持仓数量",
            content="8只股票",
            description="分散持仓",
            key="live_positions"
        )

    with col4:
        ui.metric_card(
            title="风险等级",
            content="中等",
            description="安全系数 85%",
            key="live_risk"
        )

    st.divider()

    # 持仓表格演示
    st.subheader("持仓详情")

    # 创建模拟持仓数据
    positions_data = []
    for i in range(8):
        pnl = np.random.uniform(-5000, 15000)
        positions_data.append({
            "股票代码": ["AAPL", "GOOGL", "MSFT", "000858.SZ", "600519.SS", "TSLA", "AMZN", "NVDA"][i],
            "持仓数量": np.random.randint(10, 1000),
            "平均成本": round(np.random.uniform(50, 300), 2),
            "当前价格": round(np.random.uniform(50, 300), 2),
            "市值": np.random.randint(10000, 100000),
            "浮动盈亏": pnl,
            "盈亏比例": f"{pnl/np.random.randint(50000, 200000)*100:.2f}%"
        })

    positions_df = pd.DataFrame(positions_data)

    # 使用shadcn/ui数据表格
    with ui.card(key="positions_demo"):
        ui.dataframe(
            positions_df,
            use_container_width=True,
            key="demo_positions_table"
        )

    # 图表演示
    st.subheader("数据可视化")

    tab1, tab2 = st.tabs(["📈 盈亏趋势", "🥧 持仓分布"])

    with tab1:
        # 盈亏趋势图
        dates = pd.date_range(datetime.now() - timedelta(days=30), datetime.now(), freq='D')
        pnl_values = np.cumsum(np.random.normal(1000, 5000, len(dates)))

        pnl_df = pd.DataFrame({
            '日期': dates.strftime('%m-%d'),
            '累计盈亏': pnl_values
        })

        fig_line = px.line(
            pnl_df,
            x='日期',
            y='累计盈亏',
            title='30天盈亏趋势',
            markers=True
        )

        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        # 持仓分布饼图
        pie_fig = px.pie(
            positions_df,
            values='市值',
            names='股票代码',
            title='持仓市值分布'
        )

        st.plotly_chart(pie_fig, use_container_width=True)

def show_analysis_demo():
    """技术分析演示"""
    st.header("📈 技术分析演示")

    # 股票选择和参数设置
    col1, col2, col3 = st.columns(3)

    with col1:
        analysis_stock = st.selectbox(
            "选择股票",
            ["AAPL", "GOOGL", "MSFT", "000858.SZ", "600519.SS"],
            key="analysis_stock"
        )

    with col2:
        time_period = st.selectbox(
            "时间周期",
            ["日K", "周K", "月K", "5分钟", "15分钟"],
            key="analysis_period"
        )

    with col3:
        indicators = st.multiselect(
            "技术指标",
            ["移动平均线", "MACD", "RSI", "布林带", "KDJ", "威廉指标"],
            default=["移动平均线", "MACD"],
            key="analysis_indicators"
        )

    st.divider()

    # 生成技术分析报告
    if st.button("🔍 生成分析报告", type="primary", use_container_width=True):
        with st.status("正在生成技术分析报告...", expanded=True) as status:
            st.write("📊 收集市场数据...")
            time.sleep(1)

            st.write("📈 计算技术指标...")
            time.sleep(1)

            st.write("🔍 识别交易信号...")
            time.sleep(1)

            status.update(label="✅ 分析完成！", state="complete")

        # 显示分析结果
        show_analysis_results(analysis_stock, indicators)

def show_analysis_results(stock, indicators):
    """显示技术分析结果"""
    st.subheader(f"{stock} 技术分析报告")

    # 创建多列布局显示不同指标
    cols = st.columns(len(indicators))

    for i, indicator in enumerate(indicators):
        with cols[i]:
            with ui.card(key=f"indicator_{indicator}_{i}"):
                ui.element("h6", children=[indicator], className="mb-3")

                if indicator == "移动平均线":
                    ui.element("div", children=[
                        ui.element("p", children=["MA5: 150.25"], className="mb-2"),
                        ui.element("p", children=["MA10: 149.80"], className="mb-2"),
                        ui.element("p", children=["MA20: 148.50"], className="mb-2"),
                        ui.element("span", children=["趋势: 上升"], className="badge badge-success")
                    ])
                elif indicator == "MACD":
                    ui.element("div", children=[
                        ui.element("p", children=["MACD: 1.25"], className="mb-2"),
                        ui.element("p", children=["信号线: 1.10"], className="mb-2"),
                        ui.element("p", children=["柱状图: 0.15"], className="mb-2"),
                        ui.element("span", children=["信号: 买入"], className="badge badge-success")
                    ])
                elif indicator == "RSI":
                    ui.element("div", children=[
                        ui.element("p", children=["RSI: 65.5"], className="mb-2"),
                        ui.element("p", children=["状态: 适中"], className="mb-2"),
                        ui.element("span", children=["建议: 持有"], className="badge badge-info")
                    ])
                else:
                    ui.element("div", children=[
                        ui.element("p", children=["计算中..."], className="mb-2"),
                        ui.element("span", children=["待实现"], className="badge badge-secondary")
                    ])

    # 综合评分
    st.subheader("综合评分")

    col1, col2, col3 = st.columns(3)

    with col1:
        ui.metric_card(
            title="技术评分",
            content="7.8/10",
            description="综合评价",
            key="tech_score"
        )

    with col2:
        ui.metric_card(
            title="买入信号",
            content="75%",
            description="信号强度",
            key="buy_signal"
        )

    with col3:
        ui.metric_card(
            title="投资建议",
            content="推荐买入",
            description="基于技术分析",
            key="investment_advice"
        )

def show_risk_demo():
    """风险控制演示"""
    st.header("🛡️ 风险控制演示")

    # 风险指标概览
    st.subheader("风险指标概览")

    risk_cols = st.columns(4)

    risk_indicators = [
        ("持仓风险", "15.2%", "低于警戒线", "success"),
        ("资金利用率", "68.5%", "合理水平", "info"),
        ("最大回撤", "-3.2%", "控制良好", "success"),
        ("风险评级", "A级", "低风险", "success")
    ]

    for i, (title, value, desc, status) in enumerate(risk_indicators):
        with risk_cols[i]:
            ui.metric_card(
                title=title,
                content=value,
                description=desc,
                key=f"risk_{i}"
            )

    st.divider()

    # 风险构成分析
    st.subheader("风险构成分析")

    risk_composition = pd.DataFrame({
        '风险类型': ['市场风险', '流动性风险', '集中度风险', '杠杆风险'],
        '占比': [45, 25, 20, 10]
    })

    fig_risk = px.pie(
        risk_composition,
        values='占比',
        names='风险类型',
        title='风险构成分解',
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    st.plotly_chart(fig_risk, use_container_width=True)

    # 风险预警
    st.subheader("风险预警信息")

    alerts = [
        {
            "等级": "低",
            "类型": "持仓比例预警",
            "描述": "AAPL持仓比例接近20%上限",
            "建议": "考虑减仓或分散投资",
            "颜色": "info"
        },
        {
            "等级": "中",
            "类型": "市场波动预警",
            "描述": "市场波动率升高10%",
            "建议": "谨慎交易，关注止损设置",
            "颜色": "warning"
        }
    ]

    for alert in alerts:
        if alert["颜色"] == "info":
            ui.element("div", children=[
                ui.element("span", children=[f"🔵 {alert['等级']}级预警"], className="text-blue-600 font-semibold"),
                ui.element("p", children=[f"**{alert['类型']}**: {alert['描述']}"], className="mb-2"),
                ui.element("p", children=[f"💡 建议：{alert['建议']}"], className="text-sm text-gray-600")
            ], className="mb-3 p-3 border-l-4 border-blue-500 bg-blue-50")
        elif alert["颜色"] == "warning":
            ui.element("div", children=[
                ui.element("span", children=[f"🟡 {alert['等级']}级预警"], className="text-yellow-600 font-semibold"),
                ui.element("p", children=[f"**{alert['类型']}**: {alert['描述']}"], className="mb-2"),
                ui.element("p", children=[f"💡 建议：{alert['建议']}"], className="text-sm text-gray-600")
            ], className="mb-3 p-3 border-l-4 border-yellow-500 bg-yellow-50")

def show_settings_demo():
    """系统设置演示"""
    st.header("⚙️ 系统设置演示")

    tab1, tab2, tab3 = st.tabs(["🔧 基础设置", "🤖 LLM配置", "📊 数据源"])

    with tab1:
        st.subheader("基础配置")

        with ui.card(key="basic_settings_demo"):
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("系统名称", value="TradingAgents演示", key="demo_system_name")
                st.selectbox(
                    "运行环境",
                    ["development", "testing", "production"],
                    key="demo_environment"
                )
                auto_start = st.checkbox("开机自启动", value=True, key="demo_auto_start")

            with col2:
                st.selectbox(
                    "日志级别",
                    ["DEBUG", "INFO", "WARNING", "ERROR"],
                    key="demo_log_level"
                )
                enable_backup = st.checkbox("自动备份", value=True, key="demo_backup")
                st.number_input(
                    "数据刷新间隔 (秒)",
                    min_value=1,
                    max_value=300,
                    value=5,
                    key="demo_refresh_interval"
                )

        if st.button("💾 保存基础设置", use_container_width=True):
            st.success("演示设置已保存")

    with tab2:
        st.subheader("LLM配置演示")

        # 演示不同智能体的LLM配置
        agents = ["研究员", "分析师", "交易员", "风险管理"]

        for agent in agents:
            with st.expander(f"{agent} LLM配置"):
                col1, col2 = st.columns(2)

                with col1:
                    provider = st.selectbox(
                        f"{agent}供应商",
                        ["OpenAI", "Anthropic", "Google"],
                        key=f"demo_{agent}_provider"
                    )

                    model = st.selectbox(
                        f"{agent}模型",
                        ["gpt-4o", "gpt-4o-mini", "o1-preview", "claude-3-5-sonnet"],
                        key=f"demo_{agent}_model"
                    )

                with col2:
                    temperature = st.slider(
                        f"{agent}创造性",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.7,
                        step=0.1,
                        key=f"demo_{agent}_temperature"
                    )

                    max_tokens = st.number_input(
                        f"{agent}最大token",
                        min_value=512,
                        max_value=8192,
                        value=2048,
                        key=f"demo_{agent}_max_tokens"
                    )

        if st.button("💾 保存LLM配置", use_container_width=True):
            st.success("LLM配置已保存")

    with tab3:
        st.subheader("数据源配置演示")

        with ui.card(key="data_sources_demo"):
            # 数据供应商选择
            data_providers = {
                "股票数据": ["yfinance", "alpha_vantage", "本地数据"],
                "技术指标": ["yfinance", "alpha_vantage", "本地计算"],
                "新闻数据": ["alpha_vantage", "google_news", "本地数据"]
            }

            for data_type, providers in data_providers.items():
                st.selectbox(
                    data_type,
                    providers,
                    key=f"demo_data_provider_{data_type}"
                )

            st.divider()

            # 更新频率设置
            col1, col2 = st.columns(2)
            with col1:
                realtime_interval = st.number_input(
                    "实时数据更新间隔 (秒)",
                    min_value=1,
                    max_value=60,
                    value=5,
                    key="demo_realtime_interval"
                )

            with col2:
                cache_duration = st.number_input(
                    "历史数据缓存时间 (小时)",
                    min_value=1,
                    max_value=168,
                    value=24,
                    key="demo_cache_duration"
                )

        if st.button("💾 保存数据源配置", use_container_width=True):
            st.success("数据源配置已保存")

def show_component_demo():
    """shadcn/ui组件演示"""
    st.header("🎨 shadcn/ui组件演示")

    st.info("以下展示streamlit-shadcn-ui的主要组件效果")

    # 输入组件演示
    st.subheader("输入组件")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**文本输入**")
        input_value = ui.input(
            default_value="Hello, World!",
            placeholder="请输入文本",
            key="demo_input"
        )
        st.write("输入值:", input_value)

    with col2:
        st.write("**数字输入**")
        number_value = ui.input(
            type="number",
            default_value=42,
            key="demo_number"
        )
        st.write("数字值:", number_value)

    with col3:
        st.write("**开关组件**")
        switch_value = ui.switch(
            default_checked=True,
            label="启用功能",
            key="demo_switch"
        )
        st.write("开关状态:", switch_value)

    # 选择组件演示
    st.subheader("选择组件")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**下拉选择**")
        select_value = ui.select(
            options=["苹果", "香蕉", "橙子"],
            key="demo_select"
        )
        st.write("选择值:", select_value)

    with col2:
        st.write("**单选按钮**")
        radio_options = [
            {"label": "选项A", "value": "A", "id": "r1"},
            {"label": "选项B", "value": "B", "id": "r2"},
            {"label": "选项C", "value": "C", "id": "r3"}
        ]
        radio_value = ui.radio_group(
            options=radio_options,
            default_value="B",
            key="demo_radio"
        )
        st.write("单选值:", radio_value)

    with col3:
        st.write("**复选框**")
        checkbox_value = ui.checkbox(
            checked=True,
            label="同意条款",
            key="demo_checkbox"
        )
        st.write("复选状态:", checkbox_value)

    # 显示组件演示
    st.subheader("显示组件")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**按钮组件**")
        button_clicked = ui.button(
            text="点击我",
            variant="default",
            key="demo_button"
        )
        if button_clicked:
            st.success("按钮被点击了！")

    with col2:
        st.write("**徽章组件**")
        ui.element("span", children=["新功能"], className="badge badge-primary")

    with col3:
        st.write("**进度条**")
        progress_value = ui.slider(
            default_value=[50],
            min_value=0,
            max_value=100,
            key="demo_progress_slider"
        )
        st.progress(progress_value[0] / 100)

    # 布局组件演示
    st.subheader("布局组件")

    # 卡片布局
    with ui.card(key="demo_card"):
        ui.element("h5", children=["演示卡片"], className="mb-3")
        ui.element("p", children=["这是一个使用shadcn/ui卡片组件的演示"], className="mb-3")
        ui.button(text="卡片内按钮", key="demo_card_button")

    # 标签页布局
    st.subheader("标签页演示")

    tab1, tab2, tab3 = st.tabs(["📊 数据", "📈 图表", "⚙️ 设置"])

    with tab1:
        st.write("数据内容")

    with tab2:
        # 小型图表示例
        chart_data = pd.DataFrame(
            np.random.randn(10, 2),
            columns=["X", "Y"]
        )

        fig = px.scatter(chart_data, x="X", y="Y", title="散点图演示")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.write("设置内容")

if __name__ == "__main__":
    main()