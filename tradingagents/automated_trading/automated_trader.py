"""
自动化交易主控制器
整合所有自动化交易模块，提供统一的交易接口
"""

import logging
import time
import threading
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

from .scheduler.trading_scheduler import TradingScheduler, trading_scheduler
from .monitor.market_monitor import MarketMonitor, market_monitor, PriceAlert
from .broker.simulated_broker import SimulatedBroker, simulated_broker
from .risk.risk_manager import RiskManager, DEFAULT_RISK_CONFIG

# 导入配置管理器
from ...config.config_manager import get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradingConfig:
    """自动化交易配置"""
    # 交易参数
    watchlist: List[str] = None
    initial_cash: float = 100000.0

    # 调度配置
    analysis_interval: int = 30  # 分钟
    risk_check_interval: int = 5  # 分钟

    # 风险配置
    risk_config: Dict = None

    # 启用功能
    enable_auto_trading: bool = True
    enable_risk_management: bool = True
    enable_monitoring: bool = True


class AutomatedTrader:
    """自动化交易主控制器"""

    def __init__(self, config: TradingConfig = None):
        """
        初始化自动化交易控制器

        Args:
            config: 交易配置，如果为None则从配置文件读取
        """
        # 获取系统配置
        system_config = get_config()

        # 如果没有传入配置，则使用系统配置中的交易配置
        if config is None:
            self.config = system_config.trading
        else:
            self.config = config

        # 初始化核心组件
        self.broker = SimulatedBroker(initial_cash=self.config.initial_cash)
        self.risk_manager = RiskManager(self.broker, system_config.risk_management)
        self.market_monitor = MarketMonitor(
            watchlist=self.config.watchlist,
            check_interval=60
        )

        # 交易状态
        self.is_running = False
        self.trading_thread = None

        # 统计信息
        self.daily_stats = {
            'date': date.today(),
            'orders_count': 0,
            'trades_count': 0,
            'pnl': 0.0,
            'alerts_count': 0
        }

        # 回调函数
        self.alert_callbacks: List[Callable[[Dict], None]] = []
        self.trade_callbacks: List[Callable[[Dict], None]] = []

        # 设置预警回调
        self.market_monitor.add_alert_callback(self._handle_price_alert)
        self.risk_manager.add_alert_callback(self._handle_risk_alert)

        logger.info("自动化交易控制器初始化完成")

    def start(self):
        """启动自动化交易"""
        if self.is_running:
            logger.warning("自动化交易已在运行中")
            return

        self.is_running = True

        # 启动市场监控
        if self.config.enable_monitoring:
            self.market_monitor.start_monitoring()

        # 设置定时任务
        self._setup_scheduled_tasks()

        # 启动调度器
        self.trading_scheduler.start()

        # 启动主交易循环
        self.trading_thread = threading.Thread(target=self._trading_loop, daemon=True)
        self.trading_thread.start()

        logger.info("自动化交易系统已启动")

    def stop(self):
        """停止自动化交易"""
        if not self.is_running:
            return

        self.is_running = False

        # 停止监控
        self.market_monitor.stop_monitoring()

        # 停止调度器
        self.trading_scheduler.stop()

        # 等待线程结束
        if self.trading_thread:
            self.trading_thread.join(timeout=5)

        logger.info("自动化交易系统已停止")

    def _setup_scheduled_tasks(self):
        """设置定时任务"""
        # 市场分析任务（每30分钟）
        self.trading_scheduler.add_market_analysis_task(
            task_func=self._run_market_analysis,
            interval_minutes=self.config.analysis_interval,
            task_name="market_analysis"
        )

        # 风险检查任务（每5分钟）
        self.trading_scheduler.add_portfolio_check_task(
            task_func=self._run_risk_check,
            interval_minutes=self.config.risk_check_interval,
            task_name="risk_check"
        )

        # 止损止盈检查（每分钟）
        self.trading_scheduler.add_portfolio_check_task(
            task_func=self._run_stop_loss_check,
            interval_minutes=1,
            task_name="stop_loss_check"
        )

        # 每日报告（收盘后）
        self.trading_scheduler.add_daily_report_task(
            task_func=self._generate_daily_report,
            report_time="15:30",
            task_name="daily_report"
        )

    def _trading_loop(self):
        """主交易循环"""
        logger.info("启动主交易循环...")

        while self.is_running:
            try:
                # 检查是否为交易时间
                if self.trading_scheduler.is_market_open():
                    # 执行交易逻辑
                    self._execute_trading_logic()
                else:
                    # 非交易时间，等待
                    next_open = self.trading_scheduler.get_next_market_open()
                    logger.info(f"当前非交易时间，下次开盘时间: {next_open}")

                # 每分钟检查一次
                time.sleep(60)

            except Exception as e:
                logger.error(f"交易循环异常: {str(e)}")
                time.sleep(60)

    def _run_market_analysis(self):
        """执行市场分析"""
        logger.info("执行市场分析...")

        try:
            # 这里集成原有的TradingAgents分析逻辑
            # 由于模块依赖关系，这里先做简化处理

            # 获取市场数据
            market_data = self.market_monitor.get_market_summary()

            # 检查交易信号
            for symbol in self.config.watchlist or ['AAPL']:
                # 这里应该调用TradingAgents的分析函数
                # 先用简化逻辑代替
                self._check_trading_signal(symbol)

            logger.info("市场分析完成")

        except Exception as e:
            logger.error(f"市场分析失败: {str(e)}")

    def _check_trading_signal(self, symbol: str):
        """检查交易信号（简化版）"""
        try:
            current_price = self.market_monitor.get_latest_price(symbol)

            if not current_price:
                return

            # 获取历史价格进行简单趋势分析
            price_history = self.market_monitor.get_price_history(symbol, minutes=60)

            if len(price_history) < 10:
                return

            # 简单趋势判断：最近价格上涨超过2%
            recent_prices = [data.price for data in price_history[-10:]]
            price_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]

            if price_change > 0.02:  # 上涨2%
                # 发出买入信号
                self._execute_buy_signal(symbol, current_price, 10)  # 买入10股

        except Exception as e:
            logger.error(f"检查交易信号失败 {symbol}: {str(e)}")

    def _execute_buy_signal(self, symbol: str, price: float, quantity: int):
        """执行买入信号"""
        if not self.config.enable_auto_trading:
            logger.info(f"自动交易已禁用，跳过买入信号: {symbol}")
            return

        # 风险验证
        if not self.risk_manager.validate_signal(symbol, 'BUY', quantity, price):
            logger.warning(f"买入信号未通过风险验证: {symbol}")
            return

        try:
            # 下单
            order_id = self.broker.place_order(
                symbol=symbol,
                quantity=quantity,
                side='buy',
                order_type='market'
            )

            # 更新统计
            self.daily_stats['orders_count'] += 1

            # 触发交易回调
            trade_info = {
                'type': 'BUY',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'order_id': order_id,
                'timestamp': datetime.now()
            }

            for callback in self.trade_callbacks:
                try:
                    callback(trade_info)
                except Exception as e:
                    logger.error(f"交易回调执行失败: {str(e)}")

            logger.info(f"买入订单执行成功: {symbol}, 数量: {quantity}, 订单ID: {order_id}")

        except Exception as e:
            logger.error(f"买入订单执行失败: {str(e)}")

    def _run_risk_check(self):
        """执行风险检查"""
        if not self.config.enable_risk_management:
            return

        try:
            # 检查单日亏损限制
            if not self.risk_manager.check_daily_loss_limit():
                logger.warning("触发单日亏损限制，停止交易")
                # 这里可以添加自动停止交易的逻辑

            # 检查止损止盈
            stop_orders = self.risk_manager.check_stop_loss_take_profit()
            for order in stop_orders:
                self._execute_stop_order(order)

        except Exception as e:
            logger.error(f"风险检查失败: {str(e)}")

    def _run_stop_loss_check(self):
        """执行止损止盈检查"""
        try:
            stop_orders = self.risk_manager.check_stop_loss_take_profit()
            for order in stop_orders:
                self._execute_stop_order(order)

        except Exception as e:
            logger.error(f"止损止盈检查失败: {str(e)}")

    def _execute_stop_order(self, order_info: str):
        """执行止损止盈订单"""
        try:
            # 解析订单信息，例如 "SELL_AAPL_STOPLOSS"
            parts = order_info.split('_')
            if len(parts) >= 3:
                side, symbol, order_type = parts[0], parts[1], '_'.join(parts[2:])

                # 这里简化处理，实际应该根据止损止盈类型执行
                if side == 'SELL':
                    position = self.broker.positions.get(symbol)
                    if position and position.quantity > 0:
                        order_id = self.broker.place_order(
                            symbol=symbol,
                            quantity=min(position.quantity, 100),  # 卖出全部或部分
                            side='sell',
                            order_type='market'
                        )

                        logger.info(f"止损止盈订单执行: {order_info}, 订单ID: {order_id}")

        except Exception as e:
            logger.error(f"止损止盈订单执行失败: {str(e)}")

    def _handle_price_alert(self, alert: PriceAlert):
        """处理价格预警"""
        self.daily_stats['alerts_count'] += 1

        alert_info = {
            'type': 'price_alert',
            'symbol': alert.symbol,
            'alert_type': alert.alert_type,
            'message': alert.message,
            'timestamp': alert.timestamp
        }

        # 调用预警回调
        for callback in self.alert_callbacks:
            try:
                callback(alert_info)
            except Exception as e:
                logger.error(f"预警回调执行失败: {str(e)}")

        # 如果是剧烈价格变化，可能触发交易信号
        if alert.alert_type == 'price_change' and abs(alert.change_percent) > 5.0:
            logger.info(f"大额价格变化预警，可能需要关注: {alert.symbol}")

    def _handle_risk_alert(self, alert):
        """处理风险预警"""
        self.daily_stats['alerts_count'] += 1

        alert_info = {
            'type': 'risk_alert',
            'alert_type': alert.alert_type,
            'symbol': alert.symbol,
            'message': alert.message,
            'severity': alert.severity,
            'timestamp': alert.timestamp
        }

        # 调用预警回调
        for callback in self.alert_callbacks:
            try:
                callback(alert_info)
            except Exception as e:
                logger.error(f"风险预警回调执行失败: {str(e)}")

        # 如果是严重风险，可能需要停止交易
        if alert.severity == 'critical':
            logger.critical(f"严重风险预警: {alert.message}")
            # 这里可以添加停止交易的逻辑

    def _generate_daily_report(self):
        """生成每日报告"""
        try:
            # 获取账户信息
            account_info = self.broker.get_account_info()

            # 获取持仓信息
            positions = self.broker.get_positions()

            # 计算当日盈亏（简化计算）
            initial_value = 100000.0
            current_value = account_info['total_value']
            daily_pnl = current_value - initial_value

            # 生成报告
            report = {
                'date': date.today().isoformat(),
                'initial_value': initial_value,
                'current_value': current_value,
                'daily_pnl': daily_pnl,
                'daily_pnl_ratio': daily_pnl / initial_value,
                'orders_count': self.daily_stats['orders_count'],
                'alerts_count': self.daily_stats['alerts_count'],
                'positions_count': len(positions),
                'cash_remaining': account_info['cash'],
                'top_positions': positions[:5] if positions else []
            }

            logger.info(f"每日报告: 总价值 {current_value:.2f}, 当日盈亏 {daily_pnl:.2f} ({daily_pnl/initial_value:.2%})")

            # 重置每日统计
            self.daily_stats = {
                'date': date.today(),
                'orders_count': 0,
                'trades_count': 0,
                'pnl': 0.0,
                'alerts_count': 0
            }

            return report

        except Exception as e:
            logger.error(f"生成每日报告失败: {str(e)}")
            return None

    def add_alert_callback(self, callback: Callable[[Dict], None]):
        """添加预警回调"""
        self.alert_callbacks.append(callback)

    def add_trade_callback(self, callback: Callable[[Dict], None]):
        """添加交易回调"""
        self.trade_callbacks.append(callback)

    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'is_running': self.is_running,
            'account_info': self.broker.get_account_info(),
            'positions_count': len(self.broker.positions),
            'orders_count': len(self.broker.orders),
            'daily_stats': self.daily_stats,
            'risk_summary': self.risk_manager.get_risk_summary(),
            'market_summary': self.market_monitor.get_market_summary(),
            'scheduler_status': {
                'is_running': self.trading_scheduler.is_running,
                'tasks_count': len(self.trading_scheduler.list_tasks())
            }
        }

    def manual_trade(self, symbol: str, quantity: int, side: str, order_type: str = 'market'):
        """手动交易"""
        try:
            order_id = self.broker.place_order(
                symbol=symbol,
                quantity=quantity,
                side=side,
                order_type=order_type
            )

            logger.info(f"手动交易成功: {side} {quantity} {symbol}, 订单ID: {order_id}")
            return order_id

        except Exception as e:
            logger.error(f"手动交易失败: {str(e)}")
            raise

    @property
    def trading_scheduler(self):
        """获取调度器实例"""
        return trading_scheduler


# 示例使用函数
def example_usage():
    """使用示例"""
    # 创建配置
    config = TradingConfig(
        watchlist=['AAPL', 'GOOGL', 'MSFT', '000858.SZ'],
        initial_cash=100000.0,
        analysis_interval=30,
        risk_check_interval=5
    )

    # 创建交易控制器
    trader = AutomatedTrader(config)

    # 添加回调函数（可选）
    def alert_handler(alert_info):
        print(f"预警: {alert_info}")

    def trade_handler(trade_info):
        print(f"交易: {trade_info}")

    trader.add_alert_callback(alert_handler)
    trader.add_trade_callback(trade_handler)

    # 启动交易系统
    trader.start()

    # 运行一段时间后停止
    try:
        time.sleep(300)  # 运行5分钟
    finally:
        trader.stop()

    return trader


# 全局交易控制器实例
automated_trader = AutomatedTrader()