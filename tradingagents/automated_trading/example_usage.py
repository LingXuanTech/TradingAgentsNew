#!/usr/bin/env python3
"""
自动化交易系统使用示例
演示如何使用TradingAgents自动化交易模块
"""

import time
import logging
from datetime import datetime

# 导入自动化交易模块
from tradingagents.automated_trading import (
    AutomatedTrader,
    TradingConfig,
    automated_trader,
    market_monitor,
    simulated_broker
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def basic_example():
    """基本使用示例"""
    print("=" * 60)
    print("🚀 TradingAgents 自动化交易系统 - 基本示例")
    print("=" * 60)

    # 1. 创建交易配置
    config = TradingConfig(
        watchlist=['AAPL', 'GOOGL', 'MSFT', '000858.SZ'],  # 监控股票池
        initial_cash=100000.0,  # 初始资金
        analysis_interval=30,   # 每30分钟分析一次
        risk_check_interval=5   # 每5分钟检查风险
    )

    # 2. 创建自动化交易控制器
    trader = AutomatedTrader(config)

    # 3. 添加事件回调（可选）
    def alert_handler(alert_info):
        print(f"⚠️  预警: {alert_info['message']}")

    def trade_handler(trade_info):
        print(f"📈 交易: {trade_info['type']} {trade_info['quantity']} {trade_info['symbol']}")

    trader.add_alert_callback(alert_handler)
    trader.add_trade_callback(trade_handler)

    # 4. 启动交易系统
    print("🚀 启动自动化交易系统...")
    trader.start()

    # 5. 显示系统状态
    print("\n📊 当前系统状态:")
    status = trader.get_status()
    print(f"   - 运行状态: {'✅ 运行中' if status['is_running'] else '❌ 已停止'}")
    print(f"   - 账户余额: ¥{status['account_info']['cash']:,.2f}")
    print(f"   - 持仓数量: {status['positions_count']}")
    print(f"   - 订单数量: {status['orders_count']}")

    # 6. 运行一段时间（这里设置为5分钟，实际使用时可以更长）
    print("\n⏰ 系统运行中，运行5分钟后自动停止...")
    try:
        time.sleep(300)  # 运行5分钟
    except KeyboardInterrupt:
        print("\n🛑 用户中断")

    # 7. 停止交易系统
    print("🛑 停止自动化交易系统...")
    trader.stop()

    # 8. 生成最终报告
    print("\n📋 交易报告:")
    print(f"   - 订单总数: {status['daily_stats']['orders_count']}")
    print(f"   - 预警次数: {status['daily_stats']['alerts_count']}")

    return trader


def manual_trading_example():
    """手动交易示例"""
    print("\n" + "=" * 60)
    print("📈 手动交易示例")
    print("=" * 60)

    # 获取经纪商实例
    broker = simulated_broker

    print("💰 账户信息:")
    account = broker.get_account_info()
    print(f"   - 现金: ¥{account['cash']:,.2f}")
    print(f"   - 总价值: ¥{account['total_value']:,.2f}")

    # 下单示例
    print("\n📝 执行买入订单...")
    try:
        order_id = broker.place_order(
            symbol='AAPL',
            quantity=10,
            side='buy',
            order_type='market'
        )
        print(f"   ✅ 买入订单成功，订单ID: {order_id}")
    except Exception as e:
        print(f"   ❌ 买入订单失败: {e}")

    # 查询持仓
    print("\n📊 当前持仓:")
    positions = broker.get_positions()
    if positions:
        for pos in positions:
            print(f"   - {pos['symbol']}: {pos['quantity']}股，均价¥{pos['average_price']:.2f}")
    else:
        print("   - 无持仓")

    # 查询订单
    print("\n📋 订单状态:")
    orders = broker.get_orders()
    for order in orders:
        print(f"   - {order['symbol']} {order['side']}: {order['status']}")


def monitoring_example():
    """市场监控示例"""
    print("\n" + "=" * 60)
    print("📊 市场监控示例")
    print("=" * 60)

    # 获取监控器实例
    monitor = market_monitor

    # 添加价格预警回调
    def price_alert_handler(alert):
        print(f"🚨 价格预警: {alert.message}")
        print(f"   - 股票: {alert.symbol}")
        print(f"   - 类型: {alert.alert_type}")
        print(f"   - 时间: {alert.timestamp}")

    monitor.add_alert_callback(price_alert_handler)

    # 启动监控
    print("🔍 启动市场监控...")
    monitor.start_monitoring()

    # 监控运行一段时间
    print("⏰ 监控运行中，30秒后停止...")
    time.sleep(30)

    # 停止监控
    monitor.stop_monitoring()

    # 显示监控统计
    summary = monitor.get_market_summary()
    print("
📈 监控统计:"    print(f"   - 监控股票数: {summary['total_symbols']}")
    print(f"   - 监控状态: {'✅ 运行中' if summary['monitoring'] else '❌ 已停止'}")
    print(f"   - 数据点总数: {sum(data['data_points'] for data in summary['symbols_data'].values())}")


def advanced_example():
    """高级配置示例"""
    print("\n" + "=" * 60)
    print("⚙️  高级配置示例")
    print("=" * 60)

    # 创建自定义风险配置
    from tradingagents.automated_trading.risk.risk_manager import RiskConfig

    risk_config = RiskConfig(
        max_position_per_stock=50000.0,  # 单股最大持仓5万
        max_portfolio_risk=0.3,          # 投资组合最大风险30%
        max_daily_loss=0.02,             # 单日最大亏损2%
        stop_loss_ratio=0.05,            # 止损5%
        take_profit_ratio=0.2,           # 止盈20%
        max_orders_per_day=50            # 单日最大50笔订单
    )

    # 创建高级配置
    config = TradingConfig(
        watchlist=['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', '000858.SZ', '600519.SS'],
        initial_cash=500000.0,
        analysis_interval=15,  # 更频繁的分析
        risk_config=risk_config,
        enable_auto_trading=True,
        enable_risk_management=True,
        enable_monitoring=True
    )

    # 创建交易控制器
    trader = AutomatedTrader(config)

    print("⚙️  高级配置已应用:")
    print(f"   - 监控股票: {len(config.watchlist)}只")
    print(f"   - 初始资金: ¥{config.initial_cash:,.2f}")
    print(f"   - 分析间隔: {config.analysis_interval}分钟")
    print(f"   - 单股最大持仓: ¥{risk_config.max_position_per_stock:,.2f}")
    print(f"   - 单日最大亏损: {risk_config.max_daily_loss:.2%}")

    return trader


def main():
    """主函数"""
    print("🤖 TradingAgents 自动化交易系统")
    print("这是一个演示程序，展示如何使用自动化交易模块")
    print("\n⚠️  重要提醒:")
    print("   - 此系统仅供学习和研究使用")
    print("   - 请勿用于实际交易")
    print("   - 使用前请仔细阅读相关法律法规")

    try:
        # 基本示例
        trader = basic_example()

        # 手动交易示例
        manual_trading_example()

        # 市场监控示例
        monitoring_example()

        # 高级配置示例
        advanced_trader = advanced_example()

        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("=" * 60)
        print("\n📚 接下来你可以:")
        print("   1. 修改配置参数来自定义交易策略")
        print("   2. 添加自己的交易信号生成逻辑")
        print("   3. 集成真实的经纪商API")
        print("   4. 扩展风险管理规则")
        print("   5. 添加更多技术指标和分析方法")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        logger.exception("演示错误详情")


if __name__ == "__main__":
    main()