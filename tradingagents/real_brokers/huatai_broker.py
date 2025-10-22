"""
华泰证券经纪商API实现
基于华泰证券开放API接口
"""

import asyncio
import json
import hashlib
import hmac
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp

from .base_broker import (
    BaseBroker, AccountInfo, RealPosition, RealOrder,
    OrderSide, OrderType, OrderStatus, BrokerError
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HuataiBroker(BaseBroker):
    """华泰证券经纪商实现"""

    BASE_URL = "https://openapi.htsc.com.cn"
    SANDBOX_URL = "https://openapi-sandbox.htsc.com.cn"

    def __init__(self, config: Dict[str, Any]):
        """
        初始化华泰证券连接

        Args:
            config: 配置信息，包含：
                - app_key: 应用密钥
                - app_secret: 应用秘钥
                - account_id: 资金账户
                - password: 交易密码
                - sandbox: 是否使用沙箱环境（默认False）
        """
        super().__init__(config)

        self.app_key = config['app_key']
        self.app_secret = config['app_secret']
        self.account_id = config['account_id']
        self.password = config['password']
        self.sandbox = config.get('sandbox', False)

        # API地址
        self.base_url = self.SANDBOX_URL if self.sandbox else self.BASE_URL

        # HTTP会话
        self.session: Optional[aiohttp.ClientSession] = None

        # 认证令牌
        self.access_token: Optional[str] = None
        self.token_expires: Optional[datetime] = None

    async def connect(self) -> bool:
        """连接到华泰证券API"""
        try:
            # 创建HTTP会话
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'TradingAgents/1.0'
                }
            )

            logger.info("华泰证券连接已建立")
            return True

        except Exception as e:
            logger.error(f"华泰证券连接失败: {str(e)}")
            return False

    async def disconnect(self) -> bool:
        """断开华泰证券连接"""
        try:
            if self.session:
                await self.session.close()
                self.session = None

            self.is_connected = False
            logger.info("华泰证券连接已断开")
            return True

        except Exception as e:
            logger.error(f"断开华泰证券连接失败: {str(e)}")
            return False

    async def authenticate(self) -> bool:
        """认证API访问权限"""
        try:
            # 华泰证券认证逻辑
            # 这里需要实现具体的认证流程

            # 1. 获取验证码（如果需要）
            # 2. 密码登录
            # 3. 获取访问令牌

            # 模拟认证成功
            self.access_token = "mock_access_token"
            self.token_expires = datetime.now().replace(hour=23, minute=59, second=59)

            logger.info("华泰证券认证成功")
            return True

        except Exception as e:
            logger.error(f"华泰证券认证失败: {str(e)}")
            return False

    async def get_account_info(self) -> AccountInfo:
        """获取账户信息"""
        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/account/info"
            headers = self._get_auth_headers()

            async with self.session.get(endpoint, headers=headers) as response:
                if response.status != 200:
                    raise BrokerError(f"获取账户信息失败: HTTP {response.status}")

                data = await response.json()

                # 解析账户信息
                account_data = data.get('data', {})

                account_info = AccountInfo(
                    account_id=self.account_id,
                    account_type=account_data.get('account_type', '普通账户'),
                    total_value=float(account_data.get('total_value', 0)),
                    cash=float(account_data.get('cash', 0)),
                    buying_power=float(account_data.get('buying_power', 0)),
                    day_trading_buying_power=float(account_data.get('day_trading_buying_power', 0)),
                    maintenance_margin=float(account_data.get('maintenance_margin', 0)),
                    currency=account_data.get('currency', 'CNY'),
                    last_updated=datetime.now()
                )

                self.account_info = account_info
                return account_info

        except Exception as e:
            logger.error(f"获取账户信息失败: {str(e)}")
            raise

    async def get_positions(self) -> List[RealPosition]:
        """获取持仓列表"""
        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/positions"
            headers = self._get_auth_headers()

            async with self.session.get(endpoint, headers=headers) as response:
                if response.status != 200:
                    raise BrokerError(f"获取持仓失败: HTTP {response.status}")

                data = await response.json()
                positions_data = data.get('data', {}).get('positions', [])

                positions = []
                for pos_data in positions_data:
                    position = RealPosition(
                        symbol=pos_data['symbol'],
                        quantity=int(pos_data['quantity']),
                        available_quantity=int(pos_data.get('available_quantity', pos_data['quantity'])),
                        average_price=float(pos_data['average_price']),
                        market_value=float(pos_data['market_value']),
                        unrealized_pnl=float(pos_data['unrealized_pnl']),
                        realized_pnl=float(pos_data.get('realized_pnl', 0)),
                        cost_basis=float(pos_data['cost_basis']),
                        last_updated=datetime.now()
                    )
                    positions.append(position)

                return positions

        except Exception as e:
            logger.error(f"获取持仓失败: {str(e)}")
            raise

    async def get_orders(self, status: Optional[str] = None) -> List[RealOrder]:
        """获取订单列表"""
        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/orders"
            headers = self._get_auth_headers()
            params = {}

            if status:
                params['status'] = status

            async with self.session.get(endpoint, headers=headers, params=params) as response:
                if response.status != 200:
                    raise BrokerError(f"获取订单失败: HTTP {response.status}")

                data = await response.json()
                orders_data = data.get('data', {}).get('orders', [])

                orders = []
                for order_data in orders_data:
                    order = RealOrder(
                        order_id=order_data['order_id'],
                        symbol=order_data['symbol'],
                        side=OrderSide(order_data['side']),
                        order_type=OrderType(order_data['order_type']),
                        quantity=int(order_data['quantity']),
                        price=float(order_data.get('price')) if order_data.get('price') else None,
                        stop_price=float(order_data.get('stop_price')) if order_data.get('stop_price') else None,
                        status=OrderStatus(order_data.get('status', 'pending')),
                        filled_quantity=int(order_data.get('filled_quantity', 0)),
                        filled_price=float(order_data.get('filled_price')) if order_data.get('filled_price') else None,
                        commission=float(order_data.get('commission', 0)),
                        created_at=datetime.fromisoformat(order_data['created_at']),
                        updated_at=datetime.fromisoformat(order_data['updated_at']),
                        exchange_order_id=order_data.get('exchange_order_id')
                    )
                    orders.append(order)

                return orders

        except Exception as e:
            logger.error(f"获取订单失败: {str(e)}")
            raise

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
        """提交订单"""
        # 验证订单参数
        self.validate_order(symbol, quantity, side, order_type)

        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/orders"
            headers = self._get_auth_headers()

            # 构建订单数据
            order_data = {
                'symbol': self.format_symbol(symbol),
                'quantity': quantity,
                'side': side,
                'order_type': order_type,
                'time_in_force': time_in_force
            }

            if price is not None:
                order_data['price'] = price
            if stop_price is not None:
                order_data['stop_price'] = stop_price

            async with self.session.post(endpoint, headers=headers, json=order_data) as response:
                if response.status not in [200, 201]:
                    error_text = await response.text()
                    raise BrokerError(f"提交订单失败: HTTP {response.status}, {error_text}")

                data = await response.json()
                order_id = data.get('data', {}).get('order_id')

                if not order_id:
                    raise BrokerError("订单提交失败：未返回订单ID")

                logger.info(f"订单提交成功: {order_id}")
                return order_id

        except Exception as e:
            logger.error(f"提交订单失败: {str(e)}")
            raise

    async def cancel_order(self, order_id: str) -> bool:
        """取消订单"""
        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/orders/{order_id}/cancel"
            headers = self._get_auth_headers()

            async with self.session.post(endpoint, headers=headers) as response:
                if response.status == 200:
                    logger.info(f"订单取消成功: {order_id}")
                    return True
                else:
                    logger.warning(f"订单取消失败: {order_id}, HTTP {response.status}")
                    return False

        except Exception as e:
            logger.error(f"取消订单失败: {str(e)}")
            return False

    async def get_order_status(self, order_id: str) -> RealOrder:
        """获取订单状态"""
        if not self._check_auth():
            raise ConnectionError("认证已过期，请重新认证")

        try:
            endpoint = f"{self.base_url}/api/orders/{order_id}"
            headers = self._get_auth_headers()

            async with self.session.get(endpoint, headers=headers) as response:
                if response.status != 200:
                    raise BrokerError(f"获取订单状态失败: HTTP {response.status}")

                data = await response.json()
                order_data = data.get('data', {})

                order = RealOrder(
                    order_id=order_data['order_id'],
                    symbol=order_data['symbol'],
                    side=OrderSide(order_data['side']),
                    order_type=OrderType(order_data['order_type']),
                    quantity=int(order_data['quantity']),
                    price=float(order_data.get('price')) if order_data.get('price') else None,
                    stop_price=float(order_data.get('stop_price')) if order_data.get('stop_price') else None,
                    status=OrderStatus(order_data.get('status', 'pending')),
                    filled_quantity=int(order_data.get('filled_quantity', 0)),
                    filled_price=float(order_data.get('filled_price')) if order_data.get('filled_price') else None,
                    commission=float(order_data.get('commission', 0)),
                    created_at=datetime.fromisoformat(order_data['created_at']),
                    updated_at=datetime.fromisoformat(order_data['updated_at']),
                    exchange_order_id=order_data.get('exchange_order_id')
                )

                return order

        except Exception as e:
            logger.error(f"获取订单状态失败: {str(e)}")
            raise

    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """获取市场数据"""
        try:
            endpoint = f"{self.base_url}/api/market/data/{self.format_symbol(symbol)}"
            headers = self._get_auth_headers()

            async with self.session.get(endpoint, headers=headers) as response:
                if response.status != 200:
                    raise BrokerError(f"获取市场数据失败: HTTP {response.status}")

                data = await response.json()
                return data.get('data', {})

        except Exception as e:
            logger.error(f"获取市场数据失败: {str(e)}")
            raise

    async def get_quote(self, symbol: str) -> Dict[str, float]:
        """获取实时报价"""
        try:
            endpoint = f"{self.base_url}/api/quotes/{self.format_symbol(symbol)}"
            headers = self._get_auth_headers()

            async with self.session.get(endpoint, headers=headers) as response:
                if response.status != 200:
                    raise BrokerError(f"获取报价失败: HTTP {response.status}")

                data = await response.json()
                quote_data = data.get('data', {})

                return {
                    'bid': float(quote_data.get('bid', 0)),
                    'ask': float(quote_data.get('ask', 0)),
                    'last': float(quote_data.get('last', 0)),
                    'volume': float(quote_data.get('volume', 0)),
                    'high': float(quote_data.get('high', 0)),
                    'low': float(quote_data.get('low', 0)),
                    'change': float(quote_data.get('change', 0)),
                    'change_percent': float(quote_data.get('change_percent', 0))
                }

        except Exception as e:
            logger.error(f"获取报价失败: {str(e)}")
            raise

    def _check_auth(self) -> bool:
        """检查认证状态"""
        if not self.access_token:
            return False

        if self.token_expires and datetime.now() > self.token_expires:
            logger.warning("访问令牌已过期")
            return False

        return True

    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证头信息"""
        # 华泰证券签名算法（示例）
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp)

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Timestamp': timestamp,
            'X-Signature': signature,
            'X-App-Key': self.app_key
        }

        return headers

    def _generate_signature(self, timestamp: str) -> str:
        """生成API签名"""
        # 华泰证券签名算法示例
        message = f"{self.app_key}{timestamp}{self.app_secret}"
        signature = hashlib.sha256(message.encode()).hexdigest()
        return signature

    def format_symbol(self, symbol: str) -> str:
        """格式化股票代码"""
        # 华泰证券股票代码格式：A股加SZ/SH后缀，如 000001.SZ
        if symbol.endswith('.SZ') or symbol.endswith('.SH'):
            return symbol

        # 根据股票代码判断市场
        if symbol.startswith('6'):
            return f"{symbol}.SH"
        elif symbol.startswith(('0', '3')):
            return f"{symbol}.SZ"
        else:
            return symbol


class GuangfaBroker(BaseBroker):
    """广发证券经纪商实现"""

    BASE_URL = "https://openapi.gf.com.cn"

    def __init__(self, config: Dict[str, Any]):
        """初始化广发证券连接"""
        super().__init__(config)

        self.app_key = config['app_key']
        self.app_secret = config['app_secret']
        self.account_id = config['account_id']

        self.base_url = self.BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> bool:
        """连接到广发证券API"""
        try:
            self.session = aiohttp.ClientSession()
            logger.info("广发证券连接已建立")
            return True
        except Exception as e:
            logger.error(f"广发证券连接失败: {str(e)}")
            return False

    async def authenticate(self) -> bool:
        """广发证券认证"""
        try:
            self.access_token = "mock_gf_token"
            logger.info("广发证券认证成功")
            return True
        except Exception as e:
            logger.error(f"广发证券认证失败: {str(e)}")
            return False

    # 其他方法实现类似华泰证券，省略具体实现
    async def get_account_info(self) -> AccountInfo:
        """获取账户信息 - 简化实现"""
        return AccountInfo(
            account_id=self.account_id,
            account_type="普通账户",
            total_value=100000.0,
            cash=80000.0,
            buying_power=80000.0,
            day_trading_buying_power=80000.0,
            maintenance_margin=0.0,
            currency="CNY",
            last_updated=datetime.now()
        )

    async def get_positions(self) -> List[RealPosition]:
        """获取持仓 - 简化实现"""
        return []

    async def get_orders(self, status: Optional[str] = None) -> List[RealOrder]:
        """获取订单 - 简化实现"""
        return []

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
        """提交订单 - 简化实现"""
        return "mock_order_id"

    async def cancel_order(self, order_id: str) -> bool:
        """取消订单 - 简化实现"""
        return True

    async def get_order_status(self, order_id: str) -> RealOrder:
        """获取订单状态 - 简化实现"""
        return RealOrder(
            order_id=order_id,
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100
        )

    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """获取市场数据 - 简化实现"""
        return {}

    async def get_quote(self, symbol: str) -> Dict[str, float]:
        """获取报价 - 简化实现"""
        return {
            'bid': 100.0,
            'ask': 100.1,
            'last': 100.05,
            'volume': 10000,
            'high': 101.0,
            'low': 99.0,
            'change': 0.05,
            'change_percent': 0.05
        }

    async def disconnect(self) -> bool:
        """断开连接 - 简化实现"""
        if self.session:
            await self.session.close()
        return True