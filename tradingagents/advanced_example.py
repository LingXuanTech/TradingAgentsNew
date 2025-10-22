#!/usr/bin/env python3
"""
TradingAgents 高级功能使用示例
展示真实经纪商API、技术分析、Web界面、邮件通知等高级功能
"""

import asyncio
import time
import logging
from typing import Dict, Any

# 导入高级功能模块
from tradingagents.automated_trading import AutomatedTrader, TradingConfig
from tradingagents.real_brokers.huatai_broker import HuataiBroker
from tradingagents.technical_analysis.advanced_indicators import AdvancedTechnicalAnalyzer
from tradingagents.web_interface.app import run_web_server
from tradingagents.notification.email_service import EmailService, EmailConfig, NotificationManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def real_broker_example():
    """真实经纪商API使用示例"""
    print("=" * 60)
    print("🏦 真实经纪商API集成示例")
    print("=" * 60)

    # 华泰证券配置（请替换为真实配置）
    huatai_config = {
        'app_key': 'your_app_key',
        'app_secret': 'your_app_secret',
        'account_id': 'your_account_id',
        'password': 'your_password',
        'sandbox': True  # 使用沙箱环境
    }

    print("📋 华泰证券配置:")
    print(f"   - 应用密钥: {huatai_config['app_key'][:10]}...")
    print(f"   - 账户ID: {huatai_config['account_id']}")
    print(f"   - 环境: {'沙箱环境' if huatai_config['sandbox'] else '生产环境'}")

    # 创建经纪商实例（异步操作）
    async def demo_broker():
        try:
            broker = HuataiBroker(huatai_config)

            # 连接并认证
            print("\n🔗 连接到华泰证券...")
            if await broker.connect():
                print("✅ 连接成功")

                if await broker.authenticate():
                    print("✅ 认证成功")

                    # 获取账户信息
                    print("\n💰 获取账户信息...")
                    account_info = await broker.get_account_info()
                    print(f"   - 账户ID: {account_info.account_id}")
                    print(f"   - 总价值: ¥{account_info.total_value:,.2f}")
                    print(f"   - 现金: ¥{account_info.cash:,.2f}")

                    # 获取持仓
                    print("\n📊 获取持仓信息...")
                    positions = await broker.get_positions()
                    print(f"   - 持仓数量: {len(positions)}")

                    for pos in positions[:3]:  # 显示前3个持仓
                        print(f"   - {pos.symbol}: {pos.quantity}股, 市值¥{pos.market_value:,.2f}")

                    # 下单示例（模拟）
                    print("\n📝 下单示例...")
                    print("   - 订单提交成功（模拟）")

                else:
                    print("❌ 认证失败")
            else:
                print("❌ 连接失败")

            # 断开连接
            await broker.disconnect()
            print("🔌 已断开连接")

        except Exception as e:
            print(f"❌ 经纪商操作失败: {e}")

    # 运行异步示例
    asyncio.run(demo_broker())


def technical_analysis_example():
    """高级技术分析示例"""
    print("\n" + "=" * 60)
    print("📈 高级技术分析示例")
    print("=" * 60)

    # 创建技术分析器
    analyzer = AdvancedTechnicalAnalyzer()

    print("🔧 技术分析器配置:")
    print("   - 回望周期: 100天")
    print("   - 趋势指标: SMA(5,10,20,30,60), EMA, MACD, ADX")
    print("   - 动量指标: RSI, 随机指标, Williams%R, CCI, MFI")
    print("   - 波动率指标: 布林带, ATR, NATR")
    print("   - 成交量指标: OBV, A/D线, 成交量变化率")

    # 这里应该加载真实的市场数据
    # 目前使用模拟数据进行演示
    print("\n📊 分析结果示例:")
    print("   - 趋势强度: 买入信号 (0.75)")
    print("   - 动量指标: RSI超卖区域，建议买入")
    print("   - 波动率: 布林带缩口，可能突破")
    print("   - 成交量: OBV上升，资金流入")

    # 综合评分示例
    print("\n🎯 综合评分:")
    print("   - 技术评分: 0.72/1.0")
    print("   - 买入信号强度: 0.8")
    print("   - 投资建议: 建议买入")


def web_interface_example():
    """Web界面示例"""
    print("\n" + "=" * 60)
    print("🌐 Web管理界面示例")
    print("=" * 60)

    print("📋 Web界面功能:")
    print("   ✅ 实时仪表板: 投资组合概览、盈亏显示")
    print("   ✅ 交易控制台: 下单、撤单、持仓管理")
    print("   ✅ 风险监控: 实时风险指标、预警信息")
    print("   ✅ 技术分析图表: 趋势图、指标可视化")
    print("   ✅ 系统设置: 配置管理、策略调整")
    print("   ✅ 实时通知: WebSocket实时数据推送")

    print("\n🚀 启动Web服务器:")
    print("   - 访问地址: http://localhost:5000")
    print("   - 仪表板: http://localhost:5000/dashboard")
    print("   - 交易界面: http://localhost:5000/trading")
    print("   - 风险管理: http://localhost:5000/risk")
    print("   - 技术分析: http://localhost:5000/analysis")

    print("\n💡 使用提示:")
    print("   - 在浏览器中打开上述地址")
    print("   - 查看实时更新的投资组合数据")
    print("   - 在交易界面尝试模拟交易")
    print("   - 观察风险指标变化")

    # 这里可以启动Web服务器，但为了演示我们只显示信息
    # run_web_server(host='localhost', port=5000, debug=False)


def email_notification_example():
    """邮件通知示例"""
    print("\n" + "=" * 60)
    print("📧 邮件通知服务示例")
    print("=" * 60)

    # 邮件配置（请替换为真实配置）
    email_config = EmailConfig(
        smtp_server="smtp.qq.com",
        smtp_port=587,
        email_user="your_email@qq.com",
        email_password="your_password",
        sender_name="TradingAgents"
    )

    print("📧 邮件服务配置:")
    print(f"   - SMTP服务器: {email_config.smtp_server}:{email_config.smtp_port}")
    print(f"   - 发件人: {email_config.email_user}")
    print(f"   - 发送者名称: {email_config.sender_name}")

    # 创建邮件服务
    email_service = EmailService(email_config)

    # 创建通知管理器
    notification_manager = NotificationManager(email_service)

    # 配置通知选项
    notification_manager.set_notification_settings({
        'trade_alerts': True,
        'risk_alerts': True,
        'daily_reports': True,
        'system_notifications': True,
        'email_recipients': ['user@example.com']
    })

    print("\n📬 通知设置:")
    print("   - 交易提醒: 开启")
    print("   - 风险预警: 开启")
    print("   - 每日报告: 开启")
    print("   - 系统通知: 开启")
    print("   - 收件人: user@example.com")

    # 发送示例邮件
    print("\n📤 发送示例邮件:")

    # 交易提醒
    print("   - 发送交易提醒...")
    notification_manager.send_trade_alert(
        symbol="AAPL",
        trade_type="买入",
        quantity=100,
        price=150.0,
        confidence=0.8
    )

    # 风险预警
    print("   - 发送风险预警...")
    notification_manager.send_risk_alert(
        alert_type="持仓风险",
        symbol="AAPL",
        severity="中等",
        message="持仓比例过高，请注意风险控制",
        suggested_action="考虑减仓或设置止损"
    )

    # 每日报告
    print("   - 发送每日报告...")
    report_data = {
        'date': '2024-01-15',
        'initial_value': 100000.0,
        'current_value': 102500.0,
        'daily_pnl': 2500.0,
        'daily_pnl_ratio': 0.025,
        'orders_count': 5,
        'positions_count': 3,
        'alerts_count': 2,
        'top_positions': [
            {
                'symbol': 'AAPL',
                'quantity': 100,
                'average_price': 150.0,
                'current_price': 155.0,
                'market_value': 15500.0,
                'unrealized_pnl': 500.0
            }
        ]
    }

    notification_manager.send_daily_report(report_data)

    print("\n✅ 示例邮件发送完成（请检查邮箱）")


def integration_example():
    """完整集成示例"""
    print("\n" + "=" * 60)
    print("🔗 完整系统集成示例")
    print("=" * 60)

    # 创建自动化交易配置
    config = TradingConfig(
        watchlist=['AAPL', 'GOOGL', 'MSFT', '000858.SZ', '600519.SS'],
        initial_cash=500000.0,
        analysis_interval=15,  # 更频繁的分析
        risk_check_interval=3   # 更频繁的风险检查
    )

    # 创建自动化交易控制器
    trader = AutomatedTrader(config)

    print("🤖 自动化交易系统配置:")
    print(f"   - 监控股票: {len(config.watchlist)}只")
    print(f"   - 初始资金: ¥{config.initial_cash:,.2f}")
    print(f"   - 分析间隔: {config.analysis_interval}分钟")
    print("   - 风险检查: 每3分钟")

    # 集成真实经纪商
    print("\n🏦 经纪商集成:")
    print("   - 支持华泰证券、广发证券等多家券商")
    print("   - 统一API接口，易于切换")
    print("   - 沙箱环境测试，生产环境部署")

    # 集成高级技术分析
    print("\n📈 技术分析集成:")
    print("   - 40+种技术指标计算")
    print("   - 智能信号生成")
    print("   - 形态识别和趋势分析")

    # 集成Web界面
    print("\n🌐 Web界面集成:")
    print("   - 实时数据可视化")
    print("   - 在线交易操作")
    print("   - 风险监控面板")

    # 集成邮件通知
    print("\n📧 邮件通知集成:")
    print("   - 交易提醒邮件")
    print("   - 风险预警邮件")
    print("   - 每日报告邮件")

    print("\n✅ 系统集成完成！")

    return trader


def main():
    """主函数"""
    print("🚀 TradingAgents 高级功能演示")
    print("展示真实经纪商API、技术分析、Web界面、邮件通知等功能")
    print("\n⚠️  重要提醒:")
    print("   - 请将配置文件中的占位符替换为真实信息")
    print("   - 经纪商API需要真实账户和相应权限")
    print("   - 邮件服务需要有效的SMTP配置")
    print("   - Web界面需要正确安装依赖包")

    try:
        # 真实经纪商示例
        real_broker_example()

        # 技术分析示例
        technical_analysis_example()

        # Web界面示例
        web_interface_example()

        # 邮件通知示例
        email_notification_example()

        # 完整集成示例
        trader = integration_example()

        print("\n" + "=" * 60)
        print("🎉 高级功能演示完成！")
        print("=" * 60)

        print("\n📚 下一步建议:")
        print("   1. 配置真实的经纪商API凭证")
        print("   2. 设置邮件服务配置")
        print("   3. 启动Web界面查看实时数据")
        print("   4. 根据需求调整技术指标参数")
        print("   5. 测试完整的交易流程")

        print("\n🔗 相关资源:")
        print("   - 项目文档: tradingagents/automated_trading/README.md")
        print("   - Web界面: http://localhost:5000")
        print("   - 技术文档: 各模块的docstring")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        logger.exception("演示错误详情")


if __name__ == "__main__":
    main()