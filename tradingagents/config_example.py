#!/usr/bin/env python3
"""
TradingAgents 配置管理使用示例
展示如何使用统一的配置管理系统
"""

import os
import logging
from pathlib import Path

# 导入配置管理器
from tradingagents.config.config_manager import (
    ConfigManager, get_config, load_config, save_config,
    update_config, validate_config
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def basic_config_example():
    """基本配置使用示例"""
    print("=" * 60)
    print("⚙️ 基本配置使用示例")
    print("=" * 60)

    # 1. 使用默认配置
    print("📋 加载默认配置:")
    config = get_config()
    print(f"   - 系统版本: {config.version}")
    print(f"   - 环境: {config.environment}")
    print(f"   - 股票池: {config.trading.watchlist}")
    print(f"   - 初始资金: ¥{config.trading.initial_cash:,.2f}")

    # 2. 验证配置
    print("\n🔍 验证配置:")
    errors = validate_config()
    if errors:
        print(f"   ❌ 配置错误: {errors}")
    else:
        print("   ✅ 配置验证通过")

    return config


def custom_config_example():
    """自定义配置示例"""
    print("\n" + "=" * 60)
    print("🎨 自定义配置示例")
    print("=" * 60)

    # 创建自定义配置
    custom_config = {
        'trading': {
            'watchlist': ['AAPL', 'GOOGL', 'MSFT', '000858.SZ', '600519.SS'],
            'initial_cash': 500000.0,
            'analysis_interval': 15,
            'enable_auto_trading': True
        },
        'risk_management': {
            'max_position_per_stock': 50000.0,
            'max_portfolio_risk': 0.3,
            'stop_loss_ratio': 0.05,
            'take_profit_ratio': 0.2
        },
        'email_notification': {
            'enabled': True,
            'email_user': 'your_email@qq.com',
            'email_password': 'your_password',
            'recipients': ['user@example.com']
        }
    }

    print("📝 应用自定义配置:")
    print(f"   - 股票池: {custom_config['trading']['watchlist']}")
    print(f"   - 初始资金: ¥{custom_config['trading']['initial_cash']:,.2f}")
    print(f"   - 最大持仓: ¥{custom_config['risk_management']['max_position_per_stock']:,.2f}")

    # 更新配置
    if update_config(custom_config):
        print("   ✅ 配置更新成功")

        # 重新加载配置
        updated_config = get_config()
        print(f"   - 更新后股票池: {updated_config.trading.watchlist}")
        print(f"   - 更新后资金: ¥{updated_config.trading.initial_cash:,.2f}")
    else:
        print("   ❌ 配置更新失败")


def broker_config_example():
    """经纪商配置示例"""
    print("\n" + "=" * 60)
    print("🏦 经纪商配置示例")
    print("=" * 60)

    config = get_config()

    print("📋 当前经纪商配置:")
    print(f"   - 默认经纪商: {config.broker.default_broker}")
    print(f"   - 华泰证券启用: {config.broker.huatai['enabled']}")
    print(f"   - 华泰沙箱环境: {config.broker.huatai['sandbox']}")

    # 配置华泰证券（示例）
    huatai_config = {
        'broker': {
            'huatai': {
                'enabled': True,
                'app_key': 'your_actual_app_key',
                'app_secret': 'your_actual_app_secret',
                'account_id': 'your_actual_account_id',
                'password': 'your_actual_password',
                'sandbox': False  # 生产环境设为False
            }
        }
    }

    print("
🔧 配置华泰证券:"    print(f"   - 应用密钥: {huatai_config['broker']['huatai']['app_key'][:10]}...")
    print(f"   - 账户ID: {huatai_config['broker']['huatai']['account_id']}")
    print(f"   - 环境: {'生产环境' if not huatai_config['broker']['huatai']['sandbox'] else '沙箱环境'}")

    # 这里可以调用update_config(huatai_config)来应用配置


def web_interface_config_example():
    """Web界面配置示例"""
    print("\n" + "=" * 60)
    print("🌐 Web界面配置示例")
    print("=" * 60)

    config = get_config()

    print("📋 当前Web界面配置:")
    print(f"   - 监听地址: {config.web_interface.host}")
    print(f"   - 监听端口: {config.web_interface.port}")
    print(f"   - 调试模式: {config.web_interface.debug}")
    print(f"   - 启用CORS: {config.web_interface.enable_cors}")

    print("
📊 更新间隔配置:"    for key, value in config.web_interface.update_intervals.items():
        print(f"   - {key}: {value}ms")


def email_config_example():
    """邮件配置示例"""
    print("\n" + "=" * 60)
    print("📧 邮件配置示例")
    print("=" * 60)

    config = get_config()

    print("📋 当前邮件配置:")
    print(f"   - 启用状态: {config.email_notification.enabled}")
    print(f"   - SMTP服务器: {config.email_notification.smtp_server}")
    print(f"   - 发件人: {config.email_notification.email_user}")
    print(f"   - 发送者名称: {config.email_notification.sender_name}")

    print("
📬 通知设置:"    for key, value in config.email_notification.notifications.items():
        print(f"   - {key}: {value}")

    print(f"\n👥 收件人列表: {config.email_notification.recipients}")


def config_file_operations():
    """配置文件操作示例"""
    print("\n" + "=" * 60)
    print("📁 配置文件操作示例")
    print("=" * 60)

    # 获取项目根目录
    project_root = Path(__file__).parent

    print("📂 配置文件路径:")
    print(f"   - 项目根目录: {project_root}")
    print(f"   - 默认配置: {project_root / 'config' / 'default_config.yaml'}")
    print(f"   - 用户配置: {project_root / 'config' / 'user_config.yaml'}")
    print(f"   - 配置模板: {project_root / 'config' / 'user_config_template.yaml'}")

    # 检查配置文件是否存在
    user_config_file = project_root / 'config' / 'user_config.yaml'
    if not user_config_file.exists():
        print("
💡 建议:"        print(f"   - 复制配置模板到用户配置文件: {user_config_file}")
        print("   - 修改用户配置文件以适应你的需求"
    else:
        print("   ✅ 用户配置文件已存在"
    # 显示配置验证结果
    print("
🔍 配置验证:"    errors = validate_config()
    if errors:
        print(f"   ❌ 发现 {len(errors)} 个配置错误:")
        for error in errors:
            print(f"      - {error}")
    else:
        print("   ✅ 配置验证通过")


def save_and_load_example():
    """保存和加载配置示例"""
    print("\n" + "=" * 60)
    print("💾 保存和加载配置示例")
    print("=" * 60)

    # 创建备份配置
    backup_config = {
        'trading': {
            'watchlist': ['AAPL', 'GOOGL'],
            'initial_cash': 200000.0,
            'analysis_interval': 20
        },
        'risk_management': {
            'max_position_per_stock': 30000.0,
            'max_daily_loss': 0.02
        }
    }

    print("📦 备份当前配置并应用新配置:")

    # 保存当前配置
    if save_config('config/backup_config.yaml'):
        print("   ✅ 当前配置已备份到 config/backup_config.yaml")

    # 更新配置
    if update_config(backup_config):
        print("   ✅ 新配置已应用")

        # 验证更新结果
        config = get_config()
        print(f"   - 更新后股票池: {config.trading.watchlist}")
        print(f"   - 更新后资金: ¥{config.trading.initial_cash:,.2f}")
        print(f"   - 更新后持仓限制: ¥{config.risk_management.max_position_per_stock:,.2f}")
    else:
        print("   ❌ 配置更新失败")


def main():
    """主函数"""
    print("🚀 TradingAgents 配置管理系统演示")
    print("展示统一的配置管理功能")

    try:
        # 基本配置示例
        config = basic_config_example()

        # 自定义配置示例
        custom_config_example()

        # 经纪商配置示例
        broker_config_example()

        # Web界面配置示例
        web_interface_config_example()

        # 邮件配置示例
        email_config_example()

        # 配置文件操作示例
        config_file_operations()

        # 保存和加载示例
        save_and_load_example()

        print("\n" + "=" * 60)
        print("✅ 配置管理演示完成！")
        print("=" * 60)

        print("\n📚 配置管理优势:")
        print("   ✅ 统一管理: 所有配置集中管理，避免散落")
        print("   ✅ 灵活配置: 支持多环境、多场景配置")
        print("   ✅ 类型安全: 配置项类型检查和验证")
        print("   ✅ 热更新: 不重启服务即可更新配置")
        print("   ✅ 易备份: 支持配置导入导出和版本管理")

        print("\n🔧 使用建议:")
        print("   1. 复制 user_config_template.yaml 为 user_config.yaml")
        print("   2. 根据实际需求修改 user_config.yaml")
        print("   3. 使用配置验证功能检查配置正确性")
        print("   4. 生产环境建议定期备份配置文件")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        logger.exception("演示错误详情")


if __name__ == "__main__":
    main()