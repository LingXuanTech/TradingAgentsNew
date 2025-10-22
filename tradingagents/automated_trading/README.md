# 🤖 TradingAgents 自动化交易系统

这是一个基于原有TradingAgents多智能体框架构建的自动化交易系统扩展模块，将研究型的单点决策系统改造为生产级的自动化交易解决方案。

## 🚀 核心特性

### ✅ 已完成功能
- **⏰ 定时调度器**: 支持定时执行市场分析、风险检查、止损止盈等任务
- **📊 市场监控器**: 实时监控股票价格变化、成交量异常、市场预警
- **💼 模拟交易接口**: 完整的订单管理、持仓跟踪、账户管理功能
- **🛡️ 风险管理系统**: 多层次风险控制、止损止盈、资金管理
- **🎮 主控制器**: 统一协调所有模块，提供简单易用的接口

## 📁 模块结构

```
tradingagents/automated_trading/
├── __init__.py              # 模块入口
├── automated_trader.py      # 主控制器
├── example_usage.py         # 使用示例
├── scheduler/               # 定时调度器
│   └── trading_scheduler.py
├── monitor/                 # 市场监控器
│   └── market_monitor.py
├── broker/                  # 交易接口
│   └── simulated_broker.py
├── risk/                    # 风险管理
│   └── risk_manager.py
└── README.md               # 本文档
```

## 🛠️ 快速开始

### 1. 安装依赖

```bash
# 已在主项目中添加APScheduler依赖
pip install -r requirements.txt
```

### 2. 基本使用

```python
from tradingagents.automated_trading import AutomatedTrader, TradingConfig

# 创建配置
config = TradingConfig(
    watchlist=['AAPL', 'GOOGL', 'MSFT'],
    initial_cash=100000.0,
    analysis_interval=30,  # 每30分钟分析一次
    risk_check_interval=5   # 每5分钟检查风险
)

# 创建交易控制器
trader = AutomatedTrader(config)

# 添加回调函数（可选）
def alert_handler(alert_info):
    print(f"预警: {alert_info}")

trader.add_alert_callback(alert_handler)

# 启动系统
trader.start()

# 运行一段时间后停止
import time
time.sleep(300)  # 运行5分钟
trader.stop()
```

### 3. 高级配置

```python
from tradingagents.automated_trading.risk.risk_manager import RiskConfig

# 自定义风险配置
risk_config = RiskConfig(
    max_position_per_stock=20000.0,  # 单股最大持仓2万
    max_portfolio_risk=0.25,         # 投资组合最大风险25%
    max_daily_loss=0.03,             # 单日最大亏损3%
    stop_loss_ratio=0.08,            # 止损8%
    take_profit_ratio=0.25           # 止盈25%
)

config = TradingConfig(
    watchlist=['AAPL', 'GOOGL', 'MSFT', '000858.SZ'],
    initial_cash=500000.0,
    risk_config=risk_config
)
```

## 📊 核心模块详解

### ⏰ 定时调度器 (TradingScheduler)

**功能特性**:
- 支持定时任务执行
- 交易时间控制（9:30-15:00）
- 午休时间跳过
- 多种触发器类型（间隔、定时、每周）

**常用方法**:
```python
scheduler = TradingScheduler()

# 添加市场分析任务（每30分钟）
scheduler.add_market_analysis_task(my_analysis_func, 30)

# 添加风险检查任务（每5分钟）
scheduler.add_portfolio_check_task(my_risk_func, 5)

# 添加每日报告任务
scheduler.add_daily_report_task(my_report_func, "15:30")

scheduler.start()
```

### 📊 市场监控器 (MarketMonitor)

**功能特性**:
- 实时价格监控
- 成交量异常检测
- 价格跳空检测
- 多股票同时监控

**预警类型**:
- `price_change`: 价格剧烈变化
- `volume_spike`: 成交量异常放大
- `gap_up`: 跳空高开
- `gap_down`: 跳空低开

### 💼 模拟经纪商 (SimulatedBroker)

**功能特性**:
- 完整的订单生命周期管理
- 持仓实时跟踪
- 手续费计算
- 滑点模拟

**支持订单类型**:
- 市价单 (market)
- 限价单 (limit)
- 止损单 (stop)
- 止损限价单 (stop_limit)

### 🛡️ 风险管理器 (RiskManager)

**风险控制层次**:
1. **持仓限制**: 单股最大持仓金额
2. **风险敞口**: 投资组合整体风险比例
3. **资金充足性**: 买入时检查现金余额
4. **止损止盈**: 自动执行风险控制订单

## 🎯 使用场景

### 开发测试阶段
```python
# 使用模拟经纪商进行策略测试
from tradingagents.automated_trading import simulated_broker

order_id = simulated_broker.place_order(
    symbol='AAPL',
    quantity=100,
    side='buy',
    order_type='market'
)
```

### 实盘准备阶段
```python
# 添加真实经纪商API集成
class RealBroker(SimulatedBroker):
    def place_order(self, symbol, quantity, side, order_type):
        # 集成华泰、广发等真实券商API
        return real_broker_api.place_order(...)
```

### 生产环境部署
```python
# 多环境配置管理
config = TradingConfig()
config.watchlist = load_production_watchlist()
config.risk_config = load_production_risk_config()

trader = AutomatedTrader(config)
trader.start()  # 长期运行
```

## 🔧 自定义扩展

### 添加新的交易信号

```python
class MyTradingStrategy:
    def generate_signals(self, market_data, portfolio):
        signals = []

        for symbol in market_data:
            # 你的交易信号生成逻辑
            if self.should_buy(symbol, market_data):
                signals.append(TradingSignal(
                    symbol=symbol,
                    signal_type='BUY',
                    quantity=100,
                    confidence=0.8
                ))

        return signals
```

### 添加新的风险规则

```python
class MyRiskManager(RiskManager):
    def validate_signal(self, signal):
        # 继承原有验证逻辑
        if not super().validate_signal(signal):
            return False

        # 添加自定义风险规则
        if self.check_my_custom_rule(signal):
            return False

        return True
```

## ⚠️ 重要提醒

### 法律合规
- 本系统仅供学习研究使用
- 使用前请仔细阅读相关法律法规
- 请勿用于实际交易用途

### 风险警示
- 自动化交易存在较高风险
- 建议从小资金开始测试
- 实盘前请进行充分的回测验证

### 技术依赖
- 需要稳定的网络连接
- 依赖于数据源的可靠性
- 建议部署在云服务器上运行

## 🚀 下一步计划

### 短期目标 (1-2个月)
- [ ] 集成真实经纪商API
- [ ] 添加更多技术指标
- [ ] 实现Web管理界面
- [ ] 添加邮件通知功能

### 中期目标 (2-3个月)
- [ ] 多策略组合支持
- [ ] 机器学习信号生成
- [ ] 高级回测框架
- [ ] 绩效归因分析

### 长期目标 (6个月+)
- [ ] 跨市场交易支持
- [ ] 期权期货扩展
- [ ] 算法交易策略市场
- [ ] 云端部署服务

## 📞 技术支持

如有问题或建议，请联系开发团队或提交Issue。我们致力于为社区提供更好的自动化交易解决方案。