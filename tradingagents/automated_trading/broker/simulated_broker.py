"""
模拟交易经纪商接口
用于开发和测试阶段的交易执行模拟
"""

import logging
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from zoneinfo import ZoneInfo

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"      # 待处理
    FILLED = "filled"        # 已成交
    PARTIAL_FILLED = "partial_filled"  # 部分成交
    CANCELLED = "cancelled"  # 已取消
    REJECTED = "rejected"    # 已拒绝


class OrderSide(Enum):
    """买卖方向"""
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """订单类型"""
    MARKET = "market"        # 市价单
    LIMIT = "limit"          # 限价单
    STOP = "stop"           # 止损单
    STOP_LIMIT = "stop_limit"  # 止损限价单


@dataclass
class Order:
    """订单信息"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: Optional[float] = None  # 限价单时使用
    stop_price: Optional[float] = None  # 止损单时使用
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    filled_price: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'order_id': self.order_id,
            'symbol': self.symbol,
            'side': self.side.value,
            'order_type': self.order_type.value,
            'quantity': self.quantity,
            'price': self.price,
            'stop_price': self.stop_price,
            'status': self.status.value,
            'filled_quantity': self.filled_quantity,
            'filled_price': self.filled_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class Position:
    """持仓信息"""
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'average_price': self.average_price,
            'current_price': self.current_price,
            'market_value': self.market_value,
            'unrealized_pnl': self.unrealized_pnl,
            'realized_pnl': self.realized_pnl,
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class Account:
    """账户信息"""
    account_id: str
    cash: float
    total_value: float
    day_trading_buying_power: float
    maintenance_margin: float
    currency: str = "CNY"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'account_id': self.account_id,
            'cash': self.cash,
            'total_value': self.total_value,
            'day_trading_buying_power': self.day_trading_buying_power,
            'maintenance_margin': self.maintenance_margin,
            'currency': self.currency
        }


class SimulatedBroker:
    """模拟经纪商"""

    def __init__(
        self,
        initial_cash: float = 100000.0,
        commission_per_share: float = 0.003,  # 每股手续费
        min_commission: float = 5.0,         # 最低手续费
        slippage: float = 0.001               # 滑点（0.1%）
    ):
        """
        初始化模拟经纪商

        Args:
            initial_cash: 初始资金
            commission_per_share: 每股手续费
            min_commission: 最低手续费
            slippage: 滑点比例
        """
        self.account = Account(
            account_id="SIM_ACCOUNT_001",
            cash=initial_cash,
            total_value=initial_cash,
            day_trading_buying_power=initial_cash,
            maintenance_margin=0.0
        )

        self.commission_per_share = commission_per_share
        self.min_commission = min_commission
        self.slippage = slippage

        # 订单和持仓存储
        self.orders: Dict[str, Order] = {}
        self.positions: Dict[str, Position] = {}
        self.order_history: List[Order] = []

        # 价格数据（模拟）
        self.price_data: Dict[str, float] = {}

        logger.info(f"模拟经纪商初始化完成，初始资金: {initial_cash}")

    def get_account_info(self) -> Dict[str, Any]:
        """获取账户信息"""
        # 更新持仓市值
        self._update_positions_value()

        return self.account.to_dict()

    def get_positions(self) -> List[Dict[str, Any]]:
        """获取持仓列表"""
        self._update_positions_value()
        return [pos.to_dict() for pos in self.positions.values()]

    def get_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取订单列表"""
        if status:
            orders = [order for order in self.orders.values() if order.status.value == status]
        else:
            orders = list(self.orders.values())

        return [order.to_dict() for order in orders]

    def place_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        order_type: str = "market",
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ) -> str:
        """
        下单

        Args:
            symbol: 股票代码
            quantity: 数量
            side: 买卖方向 ('buy' or 'sell')
            order_type: 订单类型 ('market', 'limit', 'stop', 'stop_limit')
            price: 价格（限价单）
            stop_price: 止损价格（止损单）

        Returns:
            订单ID
        """
        # 验证参数
        if quantity <= 0:
            raise ValueError("数量必须大于0")

        if side not in ['buy', 'sell']:
            raise ValueError("买卖方向必须是 'buy' 或 'sell'")

        if order_type not in ['market', 'limit', 'stop', 'stop_limit']:
            raise ValueError("订单类型不支持")

        # 创建订单
        order_id = str(uuid.uuid4())
        order = Order(
            order_id=order_id,
            symbol=symbol,
            side=OrderSide(side.upper()),
            order_type=OrderType(order_type.upper()),
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )

        self.orders[order_id] = order

        # 市价单立即执行
        if order_type == 'market':
            self._execute_market_order(order)
        else:
            # 限价单和止损单需要等待价格触发
            logger.info(f"限价单已创建: {order_id}, 等待价格触发")

        return order_id

    def _execute_market_order(self, order: Order):
        """执行市价单"""
        current_price = self._get_current_price(order.symbol)

        if current_price is None:
            logger.error(f"无法获取 {order.symbol} 当前价格")
            order.status = OrderStatus.REJECTED
            return

        # 计算成交价格（考虑滑点）
        if order.side == OrderSide.BUY:
            # 买入时，价格会上浮（卖方要更高的价格）
            executed_price = current_price * (1 + self.slippage)
        else:
            # 卖出时，价格会下浮（买方出价更低）
            executed_price = current_price * (1 - self.slippage)

        # 计算手续费
        commission = max(
            abs(order.quantity) * self.commission_per_share,
            self.min_commission
        )

        # 计算订单价值
        order_value = order.quantity * executed_price + commission

        # 检查资金是否充足（买入）
        if order.side == OrderSide.BUY:
            if self.account.cash < order_value:
                logger.error(f"资金不足，订单拒绝: {order.order_id}")
                order.status = OrderStatus.REJECTED
                return

        # 检查持仓是否充足（卖出）
        if order.side == OrderSide.SELL:
            current_position = self.positions.get(order.symbol)
            if current_position is None or current_position.quantity < order.quantity:
                logger.error(f"持仓不足，订单拒绝: {order.order_id}")
                order.status = OrderStatus.REJECTED
                return

        # 执行交易
        try:
            if order.side == OrderSide.BUY:
                self._execute_buy_order(order, executed_price, commission)
            else:
                self._execute_sell_order(order, executed_price, commission)

            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            order.filled_price = executed_price
            order.updated_at = datetime.now()

            logger.info(f"订单执行成功: {order.order_id}, "
                       f"价格: {executed_price:.2f}, 数量: {order.quantity}")

        except Exception as e:
            logger.error(f"订单执行失败: {order.order_id}, 错误: {str(e)}")
            order.status = OrderStatus.REJECTED

    def _execute_buy_order(self, order: Order, price: float, commission: float):
        """执行买入订单"""
        # 扣减现金
        order_cost = order.quantity * price + commission
        self.account.cash -= order_cost

        # 更新或创建持仓
        if order.symbol in self.positions:
            position = self.positions[order.symbol]
            # 加权平均价格计算
            total_quantity = position.quantity + order.quantity
            total_cost = position.quantity * position.average_price + order.quantity * price
            position.average_price = total_cost / total_quantity
            position.quantity = total_quantity
        else:
            self.positions[order.symbol] = Position(
                symbol=order.symbol,
                quantity=order.quantity,
                average_price=price,
                current_price=price,
                market_value=order.quantity * price
            )

    def _execute_sell_order(self, order: Order, price: float, commission: float):
        """执行卖出订单"""
        # 增加现金
        sell_proceeds = order.quantity * price - commission
        self.account.cash += sell_proceeds

        # 更新持仓
        if order.symbol in self.positions:
            position = self.positions[order.symbol]
            # 计算已实现盈亏
            cost_basis = order.quantity * position.average_price
            realized_pnl = (price - position.average_price) * order.quantity - commission

            position.realized_pnl += realized_pnl
            position.quantity -= order.quantity

            # 如果持仓为0，删除持仓
            if position.quantity == 0:
                del self.positions[order.symbol]

    def cancel_order(self, order_id: str) -> bool:
        """撤单"""
        if order_id not in self.orders:
            logger.warning(f"订单不存在: {order_id}")
            return False

        order = self.orders[order_id]

        if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
            logger.warning(f"订单状态不允许取消: {order_id}, 状态: {order.status.value}")
            return False

        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now()

        logger.info(f"订单已取消: {order_id}")
        return True

    def update_price(self, symbol: str, price: float):
        """更新股票价格（外部调用）"""
        self.price_data[symbol] = price

        # 检查限价单和止损单是否应该触发
        self._check_pending_orders(symbol)

    def _check_pending_orders(self, symbol: str):
        """检查待处理订单是否应该触发"""
        current_price = self.price_data.get(symbol)

        if current_price is None:
            return

        # 检查限价单
        for order in list(self.orders.values()):
            if (order.status == OrderStatus.PENDING and
                order.symbol == symbol and
                order.order_type == OrderType.LIMIT):

                should_execute = False
                if order.side == OrderSide.BUY and current_price <= order.price:
                    should_execute = True
                elif order.side == OrderSide.SELL and current_price >= order.price:
                    should_execute = True

                if should_execute:
                    self._execute_market_order(order)  # 简化为市价执行

        # 检查止损单
        for order in list(self.orders.values()):
            if (order.status == OrderStatus.PENDING and
                order.symbol == symbol and
                order.order_type == OrderType.STOP):

                should_execute = False
                if order.side == OrderSide.BUY and current_price >= order.stop_price:
                    should_execute = True
                elif order.side == OrderSide.SELL and current_price <= order.stop_price:
                    should_execute = True

                if should_execute:
                    self._execute_market_order(order)

    def _get_current_price(self, symbol: str) -> Optional[float]:
        """获取当前价格"""
        # 优先使用外部提供的价格，否则使用模拟价格
        if symbol in self.price_data:
            return self.price_data[symbol]

        # 这里可以集成真实的价格获取逻辑
        # 目前返回None，由调用者提供价格
        return None

    def _update_positions_value(self):
        """更新持仓市值"""
        total_value = self.account.cash

        for symbol, position in self.positions.items():
            current_price = self._get_current_price(symbol)
            if current_price:
                position.current_price = current_price
                position.market_value = position.quantity * current_price
                position.unrealized_pnl = (current_price - position.average_price) * position.quantity
                total_value += position.market_value
            position.updated_at = datetime.now()

        self.account.total_value = total_value
        self.account.day_trading_buying_power = self.account.cash

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """获取投资组合概览"""
        self._update_positions_value()

        summary = {
            'account': self.account.to_dict(),
            'positions_count': len(self.positions),
            'orders_count': len(self.orders),
            'total_pnl': sum(pos.unrealized_pnl + pos.realized_pnl for pos in self.positions.values()),
            'positions': self.get_positions(),
            'top_orders': self.get_orders()[:5]  # 最近5个订单
        }

        return summary


# 全局经纪商实例
simulated_broker = SimulatedBroker()