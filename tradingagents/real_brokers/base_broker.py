"""
真实经纪商API抽象基类
定义所有经纪商接口的标准规范
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderSide(Enum):
    """订单方向"""
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """订单类型"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"
    FILLED = "filled"
    PARTIAL_FILLED = "partial_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class RealOrder:
    """真实订单信息"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    filled_price: Optional[float] = None
    avg_fill_price: Optional[float] = None
    commission: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    exchange_order_id: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class RealPosition:
    """真实持仓信息"""
    symbol: str
    quantity: int
    available_quantity: int
    average_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    cost_basis: float
    last_updated: datetime


@dataclass
class AccountInfo:
    """账户信息"""
    account_id: str
    account_type: str
    total_value: float
    cash: float
    buying_power: float
    day_trading_buying_power: float
    maintenance_margin: float
    currency: str
    last_updated: datetime


class BrokerError(Exception):
    """经纪商错误基类"""
    pass


class ConnectionError(BrokerError):
    """连接错误"""
    pass


class AuthenticationError(BrokerError):
    """认证错误"""
    pass


class InsufficientFundsError(BrokerError):
    """资金不足错误"""
    pass


class MarketDataError(BrokerError):
    """市场数据错误"""
    pass


class BaseBroker(ABC):
    """真实经纪商抽象基类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化经纪商连接

        Args:
            config: 经纪商配置，包含API密钥、账户信息等
        """
        self.config = config
        self.is_connected = False
        self.session_token: Optional[str] = None
        self.account_info: Optional[AccountInfo] = None

    @abstractmethod
    async def connect(self) -> bool:
        """
        连接到经纪商API

        Returns:
            是否连接成功
        """
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """
        断开经纪商连接

        Returns:
            是否断开成功
        """
        pass

    @abstractmethod
    async def authenticate(self) -> bool:
        """
        认证API访问权限

        Returns:
            是否认证成功
        """
        pass

    @abstractmethod
    async def get_account_info(self) -> AccountInfo:
        """
        获取账户信息

        Returns:
            账户信息对象
        """
        pass

    @abstractmethod
    async def get_positions(self) -> List[RealPosition]:
        """
        获取持仓列表

        Returns:
            持仓列表
        """
        pass

    @abstractmethod
    async def get_orders(self, status: Optional[str] = None) -> List[RealOrder]:
        """
        获取订单列表

        Args:
            status: 订单状态过滤，可选

        Returns:
            订单列表
        """
        pass

    @abstractmethod
    async def place_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        order_type: str = "market",
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "day"
    ) -> str:
        """
        提交订单

        Args:
            symbol: 股票代码
            quantity: 数量
            side: 买卖方向
            order_type: 订单类型
            price: 订单价格（限价单）
            stop_price: 止损价格（止损单）
            time_in_force: 订单有效期

        Returns:
            订单ID
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """
        取消订单

        Args:
            order_id: 订单ID

        Returns:
            是否取消成功
        """
        pass

    @abstractmethod
    async def get_order_status(self, order_id: str) -> RealOrder:
        """
        获取订单状态

        Args:
            order_id: 订单ID

        Returns:
            订单对象
        """
        pass

    @abstractmethod
    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        获取市场数据

        Args:
            symbol: 股票代码

        Returns:
            市场数据字典
        """
        pass

    @abstractmethod
    async def get_quote(self, symbol: str) -> Dict[str, float]:
        """
        获取实时报价

        Args:
            symbol: 股票代码

        Returns:
            报价信息（买价、卖价、最新价等）
        """
        pass

    async def check_connection(self) -> bool:
        """
        检查连接状态

        Returns:
            是否连接正常
        """
        try:
            # 通过获取账户信息来检查连接
            await self.get_account_info()
            return True
        except Exception as e:
            logger.error(f"连接检查失败: {str(e)}")
            return False

    def format_symbol(self, symbol: str) -> str:
        """
        格式化股票代码（不同券商格式可能不同）

        Args:
            symbol: 原始股票代码

        Returns:
            格式化后的股票代码
        """
        return symbol

    def validate_order(self, symbol: str, quantity: int, side: str, order_type: str) -> bool:
        """
        验证订单参数

        Args:
            symbol: 股票代码
            quantity: 数量
            side: 买卖方向
            order_type: 订单类型

        Returns:
            是否验证通过
        """
        if quantity <= 0:
            raise ValueError("订单数量必须大于0")

        if side not in ['buy', 'sell']:
            raise ValueError("订单方向必须是 'buy' 或 'sell'")

        if order_type not in ['market', 'limit', 'stop', 'stop_limit']:
            raise ValueError("不支持的订单类型")

        return True


class BrokerFactory:
    """经纪商工厂类"""

    _brokers = {}

    @classmethod
    def register_broker(cls, name: str, broker_class: type):
        """
        注册经纪商类型

        Args:
            name: 经纪商名称
            broker_class: 经纪商类
        """
        cls._brokers[name.lower()] = broker_class
        logger.info(f"已注册经纪商: {name}")

    @classmethod
    async def create_broker(cls, broker_type: str, config: Dict[str, Any]) -> BaseBroker:
        """
        创建经纪商实例

        Args:
            broker_type: 经纪商类型（如 'huatai', 'guangfa'）
            config: 配置信息

        Returns:
            经纪商实例
        """
        broker_class = cls._brokers.get(broker_type.lower())
        if not broker_class:
            raise ValueError(f"不支持的经纪商类型: {broker_type}")

        broker = broker_class(config)

        # 尝试连接和认证
        if await broker.connect() and await broker.authenticate():
            logger.info(f"经纪商 {broker_type} 连接成功")
            return broker
        else:
            raise ConnectionError(f"经纪商 {broker_type} 连接失败")

    @classmethod
    def get_supported_brokers(cls) -> List[str]:
        """获取支持的经纪商列表"""
        return list(cls._brokers.keys())


# 注册默认经纪商（将在具体实现中注册）
def register_default_brokers():
    """注册默认经纪商"""
    try:
        from .huatai_broker import HuataiBroker
        BrokerFactory.register_broker("huatai", HuataiBroker)
    except ImportError:
        logger.warning("华泰经纪商模块未找到")

    try:
        from .guangfa_broker import GuangfaBroker
        BrokerFactory.register_broker("guangfa", GuangfaBroker)
    except ImportError:
        logger.warning("广发经纪商模块未找到")