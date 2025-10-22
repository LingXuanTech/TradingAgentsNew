"""
自动化交易模块
提供完整的自动化交易解决方案
"""

from .automated_trader import AutomatedTrader, TradingConfig
from .scheduler.trading_scheduler import TradingScheduler
from .monitor.market_monitor import MarketMonitor, PriceAlert
from .broker.simulated_broker import SimulatedBroker, Order, Position, Account
from .risk.risk_manager import RiskManager, RiskConfig, RiskAlert

# 全局实例
from .automated_trader import automated_trader
from .scheduler.trading_scheduler import trading_scheduler
from .monitor.market_monitor import market_monitor
from .broker.simulated_broker import simulated_broker

__version__ = "1.0.0"

__all__ = [
    # 主控制器
    "AutomatedTrader",
    "TradingConfig",

    # 调度器
    "TradingScheduler",
    "trading_scheduler",

    # 监控器
    "MarketMonitor",
    "PriceAlert",
    "market_monitor",

    # 经纪商
    "SimulatedBroker",
    "Order",
    "Position",
    "Account",
    "simulated_broker",

    # 风险管理
    "RiskManager",
    "RiskConfig",
    "RiskAlert",

    # 全局实例
    "automated_trader",
]