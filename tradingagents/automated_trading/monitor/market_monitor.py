"""
市场监控器模块
负责监控股票价格、市场异常、交易信号等
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

import yfinance as yf
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PriceAlert:
    """价格预警信息"""
    symbol: str
    alert_type: str  # 'price_change', 'volume_spike', 'gap_up', 'gap_down'
    current_price: float
    previous_price: float
    change_percent: float
    timestamp: datetime
    message: str


@dataclass
class MarketData:
    """市场数据快照"""
    symbol: str
    timestamp: datetime
    price: float
    volume: int
    high: float
    low: float
    change_percent: float
    volume_ratio: float = 1.0  # 相对平均成交量的比率


class MarketMonitor:
    """市场监控器"""

    def __init__(
        self,
        watchlist: List[str],
        check_interval: int = 60,  # 检查间隔（秒）
        price_change_threshold: float = 3.0,  # 价格变化阈值（%）
        volume_spike_threshold: float = 2.0   # 成交量异常阈值（倍数）
    ):
        """
        初始化市场监控器

        Args:
            watchlist: 监控股票列表
            check_interval: 检查间隔（秒）
            price_change_threshold: 价格变化阈值（%）
            volume_spike_threshold: 成交量异常阈值（倍数）
        """
        self.watchlist = watchlist
        self.check_interval = check_interval
        self.price_change_threshold = price_change_threshold
        self.volume_spike_threshold = volume_spike_threshold

        # 监控状态
        self.is_monitoring = False
        self.monitor_thread = None

        # 数据存储
        self.price_history: Dict[str, List[MarketData]] = {}
        self.alert_callbacks: List[Callable[[PriceAlert], None]] = []

        # 成交量基准（过去20天的平均成交量）
        self.volume_baseline: Dict[str, float] = {}

        # 初始化价格历史
        self._initialize_price_history()

    def _initialize_price_history(self):
        """初始化价格历史数据"""
        logger.info("初始化价格历史数据...")
        for symbol in self.watchlist:
            self.price_history[symbol] = []

        # 获取基准成交量（过去20天平均）
        self._update_volume_baseline()

    def _update_volume_baseline(self):
        """更新成交量基准"""
        for symbol in self.watchlist:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="1mo")  # 获取一个月数据

                if not hist.empty:
                    avg_volume = hist['Volume'].mean()
                    self.volume_baseline[symbol] = avg_volume
                    logger.info(f"{symbol} 基准成交量: {avg_volume:.0f}")
                else:
                    logger.warning(f"无法获取 {symbol} 的历史数据")
                    self.volume_baseline[symbol] = 100000  # 默认值

            except Exception as e:
                logger.error(f"获取 {symbol} 基准数据失败: {str(e)}")
                self.volume_baseline[symbol] = 100000

    def start_monitoring(self):
        """启动监控"""
        if self.is_monitoring:
            logger.warning("市场监控已在运行中")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("市场监控已启动")

    def stop_monitoring(self):
        """停止监控"""
        if not self.is_monitoring:
            return

        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        logger.info("市场监控已停止")

    def _monitor_loop(self):
        """监控主循环"""
        logger.info("开始市场监控循环...")

        while self.is_monitoring:
            try:
                self._check_market_data()
                time.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"监控循环异常: {str(e)}")
                time.sleep(self.check_interval)

    def _check_market_data(self):
        """检查市场数据"""
        current_time = datetime.now(ZoneInfo("Asia/Shanghai"))

        for symbol in self.watchlist:
            try:
                # 获取最新价格数据
                stock = yf.Ticker(symbol)
                info = stock.history(period="1d", interval="1m")

                if info.empty:
                    continue

                latest_data = info.iloc[-1]
                current_price = latest_data['Close']
                current_volume = latest_data['Volume']

                # 获取前一个数据点用于比较
                previous_price = None
                if len(self.price_history[symbol]) > 0:
                    previous_price = self.price_history[symbol][-1].price

                # 创建市场数据快照
                market_data = MarketData(
                    symbol=symbol,
                    timestamp=current_time,
                    price=current_price,
                    volume=int(current_volume),
                    high=latest_data['High'],
                    low=latest_data['Low'],
                    change_percent=0.0  # 先设为0，后面计算
                )

                # 计算价格变化百分比
                if previous_price:
                    market_data.change_percent = (
                        (current_price - previous_price) / previous_price * 100
                    )

                # 检测价格异常
                self._detect_price_anomalies(symbol, market_data)

                # 检测成交量异常
                self._detect_volume_anomalies(symbol, market_data)

                # 更新价格历史（保留最近100个数据点）
                self.price_history[symbol].append(market_data)
                if len(self.price_history[symbol]) > 100:
                    self.price_history[symbol] = self.price_history[symbol][-100:]

            except Exception as e:
                logger.error(f"检查 {symbol} 市场数据失败: {str(e)}")

    def _detect_price_anomalies(self, symbol: str, market_data: MarketData):
        """检测价格异常"""
        # 价格剧烈变化预警
        if abs(market_data.change_percent) >= self.price_change_threshold:
            alert = PriceAlert(
                symbol=symbol,
                alert_type='price_change',
                current_price=market_data.price,
                previous_price=market_data.price / (1 + market_data.change_percent/100),
                change_percent=market_data.change_percent,
                timestamp=market_data.timestamp,
                message=f"{symbol} 价格变化异常: {market_data.change_percent:.2f}%"
            )
            self._trigger_alert(alert)

        # 跳空高开
        if len(self.price_history[symbol]) > 1:
            prev_close = self.price_history[symbol][-2].price
            gap_percent = (market_data.price - prev_close) / prev_close * 100

            if gap_percent >= 2.0:  # 跳空高开超过2%
                alert = PriceAlert(
                    symbol=symbol,
                    alert_type='gap_up',
                    current_price=market_data.price,
                    previous_price=prev_close,
                    change_percent=gap_percent,
                    timestamp=market_data.timestamp,
                    message=f"{symbol} 跳空高开: {gap_percent:.2f}%"
                )
                self._trigger_alert(alert)

            elif gap_percent <= -2.0:  # 跳空低开超过2%
                alert = PriceAlert(
                    symbol=symbol,
                    alert_type='gap_down',
                    current_price=market_data.price,
                    previous_price=prev_close,
                    change_percent=gap_percent,
                    timestamp=market_data.timestamp,
                    message=f"{symbol} 跳空低开: {gap_percent:.2f}%"
                )
                self._trigger_alert(alert)

    def _detect_volume_anomalies(self, symbol: str, market_data: MarketData):
        """检测成交量异常"""
        if symbol in self.volume_baseline and self.volume_baseline[symbol] > 0:
            volume_ratio = market_data.volume / self.volume_baseline[symbol]

            if volume_ratio >= self.volume_spike_threshold:
                alert = PriceAlert(
                    symbol=symbol,
                    alert_type='volume_spike',
                    current_price=market_data.price,
                    previous_price=market_data.price,
                    change_percent=0.0,
                    timestamp=market_data.timestamp,
                    message=f"{symbol} 成交量异常: {volume_ratio:.1f}倍于基准水平"
                )
                self._trigger_alert(alert)

    def _trigger_alert(self, alert: PriceAlert):
        """触发预警"""
        logger.warning(f"市场预警: {alert.message}")

        # 调用所有预警回调函数
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"预警回调执行失败: {str(e)}")

    def add_alert_callback(self, callback: Callable[[PriceAlert], None]):
        """添加预警回调函数"""
        self.alert_callbacks.append(callback)
        logger.info(f"已添加预警回调函数: {callback.__name__}")

    def get_latest_price(self, symbol: str) -> Optional[float]:
        """获取最新价格"""
        if symbol in self.price_history and self.price_history[symbol]:
            return self.price_history[symbol][-1].price
        return None

    def get_price_history(self, symbol: str, minutes: int = 60) -> List[MarketData]:
        """获取价格历史"""
        if symbol not in self.price_history:
            return []

        # 返回指定时间内的数据
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            data for data in self.price_history[symbol]
            if data.timestamp >= cutoff_time
        ]

    def get_market_summary(self) -> Dict[str, Any]:
        """获取市场概况"""
        summary = {
            'total_symbols': len(self.watchlist),
            'monitoring': self.is_monitoring,
            'last_update': datetime.now(),
            'symbols_data': {}
        }

        for symbol in self.watchlist:
            latest_data = self.get_latest_price(symbol)
            if latest_data:
                summary['symbols_data'][symbol] = {
                    'latest_price': latest_data,
                    'data_points': len(self.price_history[symbol])
                }

        return summary

    def force_refresh_baseline(self):
        """强制刷新成交量基准"""
        logger.info("强制刷新成交量基准...")
        self._update_volume_baseline()


# 预定义股票池（示例）
DEFAULT_WATCHLIST = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',  # 美股科技股
    '000858.SZ', '600519.SS', '000001.SZ',     # A股核心股票
]


# 全局监控器实例
market_monitor = MarketMonitor(DEFAULT_WATCHLIST)