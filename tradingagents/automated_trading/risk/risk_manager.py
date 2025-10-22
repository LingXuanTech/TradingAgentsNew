"""
风险管理模块
负责交易风险控制、止损机制、资金管理等
"""

import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from ..broker.simulated_broker import SimulatedBroker, Position, Order

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RiskConfig:
    """风险配置"""
    max_position_per_stock: float = 10000.0    # 单股最大持仓价值
    max_portfolio_risk: float = 0.2            # 投资组合最大风险比例（20%）
    max_daily_loss: float = 0.05               # 单日最大亏损比例（5%）
    stop_loss_ratio: float = 0.1               # 止损比例（10%）
    take_profit_ratio: float = 0.3             # 止盈比例（30%）
    max_orders_per_day: int = 10               # 单日最大订单数量
    min_order_interval: int = 300              # 最小下单间隔（秒）


@dataclass
class RiskAlert:
    """风险预警"""
    alert_type: str  # 'stop_loss', 'take_profit', 'position_limit', 'daily_loss'
    symbol: str
    message: str
    severity: str    # 'low', 'medium', 'high', 'critical'
    timestamp: datetime
    suggested_action: str


class RiskManager:
    """风险管理器"""

    def __init__(self, broker: SimulatedBroker, config: RiskConfig = None):
        """
        初始化风险管理器

        Args:
            broker: 经纪商实例
            config: 风险配置
        """
        self.broker = broker
        self.config = config or RiskConfig()

        # 风险监控状态
        self.daily_pnl: List[float] = []
        self.daily_orders: List[Order] = []
        self.alert_callbacks: List[Callable[[RiskAlert], None]] = []

        # 持仓止损价位追踪
        self.stop_loss_prices: Dict[str, float] = {}
        self.take_profit_prices: Dict[str, float] = {}

        logger.info("风险管理器初始化完成")

    def validate_signal(self, symbol: str, signal_type: str, quantity: int, price: float) -> bool:
        """
        验证交易信号是否符合风险控制要求

        Args:
            symbol: 股票代码
            signal_type: 信号类型 ('BUY' or 'SELL')
            quantity: 交易数量
            price: 交易价格

        Returns:
            是否通过验证
        """
        # 1. 检查单股持仓限制
        if not self._check_position_limit(symbol, quantity, price, signal_type):
            return False

        # 2. 检查投资组合风险敞口
        if not self._check_portfolio_exposure(symbol, quantity, price, signal_type):
            return False

        # 3. 检查单日订单限制
        if not self._check_daily_order_limit():
            return False

        # 4. 检查资金充足性
        if not self._check_cash_availability(symbol, quantity, price, signal_type):
            return False

        return True

    def _check_position_limit(self, symbol: str, quantity: int, price: float, signal_type: str) -> bool:
        """检查单股持仓限制"""
        order_value = quantity * price
        account_info = self.broker.get_account_info()

        # 检查是否会超过单股持仓限制
        if signal_type == 'BUY':
            if order_value > self.config.max_position_per_stock:
                self._trigger_alert(
                    RiskAlert(
                        alert_type='position_limit',
                        symbol=symbol,
                        message=f"买入订单价值({order_value:.2f})超过单股最大持仓限制({self.config.max_position_per_stock:.2f})",
                        severity='medium',
                        timestamp=datetime.now(),
                        suggested_action='减少交易数量或选择其他股票'
                    )
                )
                return False

        return True

    def _check_portfolio_exposure(self, symbol: str, quantity: int, price: float, signal_type: str) -> bool:
        """检查投资组合风险敞口"""
        order_value = quantity * price
        account_info = self.broker.get_account_info()
        portfolio_value = account_info['total_value']

        # 计算新的风险敞口比例
        if signal_type == 'BUY':
            new_exposure = order_value / portfolio_value
        else:
            # 卖出时，减少敞口
            current_position = self.broker.positions.get(symbol)
            if current_position:
                current_exposure = current_position.market_value / portfolio_value
                new_exposure = current_exposure - (quantity * price) / portfolio_value
            else:
                new_exposure = 0

        if new_exposure > self.config.max_portfolio_risk:
            self._trigger_alert(
                RiskAlert(
                    alert_type='portfolio_exposure',
                    symbol=symbol,
                    message=f"投资组合风险敞口({new_exposure:.2%})超过最大限制({self.config.max_portfolio_risk:.2%})",
                    severity='high',
                    timestamp=datetime.now(),
                    suggested_action='减少交易规模或降低整体仓位'
                )
            )
            return False

        return True

    def _check_daily_order_limit(self) -> bool:
        """检查单日订单限制"""
        today = datetime.now().date()

        # 筛选今天的订单
        today_orders = [
            order for order in self.broker.orders.values()
            if order.created_at.date() == today and order.status.value == 'filled'
        ]

        if len(today_orders) >= self.config.max_orders_per_day:
            self._trigger_alert(
                RiskAlert(
                    alert_type='daily_order_limit',
                    symbol='ALL',
                    message=f"今日订单数量({len(today_orders)})已达到最大限制({self.config.max_orders_per_day})",
                    severity='medium',
                    timestamp=datetime.now(),
                    suggested_action='等待明天再进行交易或取消部分挂单'
                )
            )
            return False

        return True

    def _check_cash_availability(self, symbol: str, quantity: int, price: float, signal_type: str) -> bool:
        """检查资金充足性"""
        if signal_type == 'BUY':
            account_info = self.broker.get_account_info()
            order_cost = quantity * price * 1.003  # 包含手续费

            if account_info['cash'] < order_cost:
                self._trigger_alert(
                    RiskAlert(
                        alert_type='insufficient_cash',
                        symbol=symbol,
                        message=f"现金不足，需要{order_cost:.2f}，可用{account_info['cash']:.2f}",
                        severity='high',
                        timestamp=datetime.now(),
                        suggested_action='减少交易数量或卖出部分持仓释放资金'
                    )
                )
                return False

        return True

    def check_stop_loss_take_profit(self) -> List[str]:
        """
        检查止损和止盈条件

        Returns:
            需要执行的订单ID列表
        """
        orders_to_execute = []

        for symbol, position in self.broker.positions.items():
            current_price = position.current_price

            # 检查止损
            if symbol in self.stop_loss_prices:
                stop_price = self.stop_loss_prices[symbol]
                if position.quantity > 0 and current_price <= stop_price:
                    logger.warning(f"{symbol} 触发止损: 当前价格{current_price} <= 止损价{stop_price}")
                    orders_to_execute.append(f"SELL_{symbol}_STOPLOSS")

            # 检查止盈
            if symbol in self.take_profit_prices:
                profit_price = self.take_profit_prices[symbol]
                if position.quantity > 0 and current_price >= profit_price:
                    logger.info(f"{symbol} 触发止盈: 当前价格{current_price} >= 止盈价{profit_price}")
                    orders_to_execute.append(f"SELL_{symbol}_TAKEPROFIT")

        return orders_to_execute

    def set_stop_loss(self, symbol: str, stop_price: float):
        """设置止损价位"""
        self.stop_loss_prices[symbol] = stop_price
        logger.info(f"为 {symbol} 设置止损价位: {stop_price}")

    def set_take_profit(self, symbol: str, profit_price: float):
        """设置止盈价位"""
        self.take_profit_prices[symbol] = profit_price
        logger.info(f"为 {symbol} 设置止盈价位: {profit_price}")

    def calculate_position_stop_loss(self, symbol: str, position_price: float) -> float:
        """计算持仓止损价位"""
        return position_price * (1 - self.config.stop_loss_ratio)

    def calculate_position_take_profit(self, symbol: str, position_price: float) -> float:
        """计算持仓止盈价位"""
        return position_price * (1 + self.config.take_profit_ratio)

    def check_daily_loss_limit(self) -> bool:
        """检查单日亏损限制"""
        account_info = self.broker.get_account_info()

        # 这里简化处理，实际应该计算当日盈亏
        # 目前使用总价值变化作为参考
        total_value = account_info['total_value']
        initial_value = 100000.0  # 假设初始价值

        daily_loss_ratio = (total_value - initial_value) / initial_value

        if daily_loss_ratio <= -self.config.max_daily_loss:
            self._trigger_alert(
                RiskAlert(
                    alert_type='daily_loss_limit',
                    symbol='ALL',
                    message=f"单日亏损({daily_loss_ratio:.2%})超过最大限制({-self.config.max_daily_loss:.2%})",
                    severity='critical',
                    timestamp=datetime.now(),
                    suggested_action='停止当日交易，等待明天重新评估'
                )
            )
            return False

        return True

    def add_alert_callback(self, callback: Callable[[RiskAlert], None]):
        """添加风险预警回调"""
        self.alert_callbacks.append(callback)
        logger.info(f"已添加风险预警回调: {callback.__name__}")

    def _trigger_alert(self, alert: RiskAlert):
        """触发风险预警"""
        logger.warning(f"风险预警[{alert.severity.upper()}]: {alert.message}")

        # 调用所有预警回调函数
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"风险预警回调执行失败: {str(e)}")

    def get_risk_summary(self) -> Dict[str, Any]:
        """获取风险概览"""
        account_info = self.broker.get_account_info()
        positions = self.broker.get_positions()

        # 计算持仓风险指标
        total_position_value = sum(pos['market_value'] for pos in positions)
        total_portfolio_value = account_info['total_value']

        # 计算各股票持仓比例
        position_ratios = {}
        for pos in positions:
            ratio = pos['market_value'] / total_portfolio_value
            position_ratios[pos['symbol']] = {
                'value': pos['market_value'],
                'ratio': ratio,
                'unrealized_pnl': pos['unrealized_pnl']
            }

        return {
            'account_info': account_info,
            'total_positions': len(positions),
            'total_position_value': total_position_value,
            'cash_ratio': account_info['cash'] / total_portfolio_value,
            'position_ratios': position_ratios,
            'stop_loss_count': len(self.stop_loss_prices),
            'take_profit_count': len(self.take_profit_prices),
            'risk_config': {
                'max_position_per_stock': self.config.max_position_per_stock,
                'max_portfolio_risk': self.config.max_portfolio_risk,
                'max_daily_loss': self.config.max_daily_loss,
                'stop_loss_ratio': self.config.stop_loss_ratio,
                'take_profit_ratio': self.config.take_profit_ratio
            }
        }

    def auto_set_risk_levels(self):
        """自动设置风险水平"""
        """为所有持仓自动设置止损和止盈价位"""
        for symbol, position in self.broker.positions.items():
            # 设置止损价位
            stop_price = self.calculate_position_stop_loss(symbol, position.average_price)
            self.set_stop_loss(symbol, stop_price)

            # 设置止盈价位
            profit_price = self.calculate_position_take_profit(symbol, position.average_price)
            self.set_take_profit(symbol, profit_price)

        logger.info(f"已为 {len(self.broker.positions)} 个持仓自动设置风险水平")


# 默认风险配置
DEFAULT_RISK_CONFIG = RiskConfig(
    max_position_per_stock=20000.0,    # 单股最大2万
    max_portfolio_risk=0.25,           # 投资组合最大风险25%
    max_daily_loss=0.03,              # 单日最大亏损3%
    stop_loss_ratio=0.08,             # 止损8%
    take_profit_ratio=0.25,           # 止盈25%
    max_orders_per_day=20,            # 单日最大20笔订单
    min_order_interval=60             # 最小下单间隔1分钟
)