# ⚙️ TradingAgents 配置管理系统

## 概述

TradingAgents 采用统一的配置管理系统，将所有模块的配置集中管理，提供灵活的配置方式和热更新功能。

## 📁 配置文件结构

```
tradingagents/config/
├── config_manager.py           # 配置管理器核心类
├── default_config.yaml         # 默认配置文件
├── user_config_template.yaml   # 用户配置模板
├── README.md                   # 本文档
└── user_config.yaml           # 用户自定义配置（运行时生成）
```

## 🚀 快速开始

### 1. 复制配置模板

```bash
# 复制模板文件
cp tradingagents/config/user_config_template.yaml tradingagents/config/user_config.yaml
```

### 2. 编辑配置

使用文本编辑器打开 `user_config.yaml` 并根据需要修改配置：

```bash
nano tradingagents/config/user_config.yaml
```

### 3. 验证配置

```python
from tradingagents.config.config_manager import validate_config

# 验证配置
errors = validate_config()
if errors:
    print("配置错误:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ 配置验证通过")
```

## 📋 配置项详解

### 基本配置

```yaml
version: "2.0.0"                    # 系统版本
environment: "development"          # 运行环境: development, testing, production
```

### 自动化交易配置

```yaml
trading:
  watchlist:                        # 监控股票池
    - "AAPL"
    - "GOOGL"
    - "MSFT"
  initial_cash: 100000.0            # 初始资金 (人民币)
  analysis_interval: 30             # 分析间隔 (分钟)
  risk_check_interval: 5            # 风险检查间隔 (分钟)
  enable_auto_trading: true         # 启用自动交易
  enable_risk_management: true      # 启用风险管理
  enable_monitoring: true           # 启用市场监控
```

### 经纪商配置

```yaml
broker:
  huatai:                           # 华泰证券配置
    enabled: false                  # 是否启用
    app_key: "YOUR_APP_KEY"         # 应用密钥
    app_secret: "YOUR_APP_SECRET"   # 应用秘钥
    account_id: "YOUR_ACCOUNT_ID"   # 资金账户
    password: "YOUR_PASSWORD"       # 交易密码
    sandbox: true                   # 是否沙箱环境

  guangfa:                          # 广发证券配置
    enabled: false                  # 是否启用
    app_key: "YOUR_APP_KEY"         # 应用密钥
    app_secret: "YOUR_APP_SECRET"   # 应用秘钥
    account_id: "YOUR_ACCOUNT_ID"   # 资金账户
    password: "YOUR_PASSWORD"       # 交易密码

  default_broker: "huatai"          # 默认经纪商
```

### 技术分析配置

```yaml
technical_analysis:
  lookback_period: 100              # 回望周期 (天)
  enable_advanced_indicators: true  # 启用高级指标
  enable_pattern_recognition: true  # 启用形态识别
  signal_threshold: 0.6             # 信号阈值

  trend_indicators:                 # 趋势指标参数
    sma_periods: [5, 10, 20, 30, 60]
    ema_periods: [5, 10, 20, 30, 60]
    macd:
      fast: 12
      slow: 26
      signal: 9

  momentum_indicators:              # 动量指标参数
    rsi_period: 14
    stoch_k: 14
    stoch_d: 3
    # ... 更多动量指标配置
```

### Web界面配置

```yaml
web_interface:
  host: "localhost"                 # 监听地址
  port: 5000                        # 监听端口
  debug: false                      # 调试模式
  enable_cors: true                 # 启用CORS

  update_intervals:                 # 更新间隔 (毫秒)
    market_data: 5000               # 市场数据
    portfolio: 10000                # 投资组合
    orders: 2000                   # 订单状态
    alerts: 3000                   # 预警信息
```

### 邮件通知配置

```yaml
email_notification:
  enabled: false                    # 是否启用邮件通知
  smtp_server: "smtp.qq.com"        # SMTP服务器
  smtp_port: 587                    # SMTP端口
  email_user: "your_email@qq.com"   # 发件人邮箱
  email_password: "your_password"   # 邮箱密码或授权码
  use_tls: true                     # 使用TLS加密
  sender_name: "TradingAgents"      # 发件人名称

  notifications:                    # 通知类型开关
    trade_alerts: true              # 交易提醒
    risk_alerts: true               # 风险预警
    daily_reports: true             # 每日报告
    system_notifications: true      # 系统通知

  recipients:                       # 收件人列表
    - "user@example.com"
```

### 风险管理配置

```yaml
risk_management:
  max_position_per_stock: 20000.0   # 单股最大持仓价值
  max_portfolio_risk: 0.25          # 投资组合最大风险比例
  max_daily_loss: 0.03              # 单日最大亏损比例
  stop_loss_ratio: 0.08             # 止损比例
  take_profit_ratio: 0.25           # 止盈比例
  max_orders_per_day: 20            # 单日最大订单数量
  min_order_interval: 60            # 最小下单间隔 (秒)
  enable_dynamic_stop_loss: true    # 启用动态止损
  enable_trailing_stop: false       # 启用追踪止损
```

## 🔧 使用示例

### 基本使用

```python
from tradingagents.config.config_manager import get_config

# 获取当前配置
config = get_config()

# 访问配置项
print(f"股票池: {config.trading.watchlist}")
print(f"初始资金: ¥{config.trading.initial_cash}")
print(f"默认经纪商: {config.broker.default_broker}")
```

### 动态更新配置

```python
from tradingagents.config.config_manager import update_config

# 更新交易配置
new_config = {
    'trading': {
        'watchlist': ['AAPL', 'GOOGL', 'TSLA'],
        'analysis_interval': 15
    },
    'risk_management': {
        'max_position_per_stock': 30000.0
    }
}

# 应用新配置
if update_config(new_config):
    print("配置更新成功")
else:
    print("配置更新失败")
```

### 保存配置

```python
from tradingagents.config.config_manager import save_config

# 保存当前配置到文件
if save_config():
    print("配置保存成功")
else:
    print("配置保存失败")
```

### 备份和恢复配置

```python
from tradingagents.config.config_manager import save_config, load_config

# 备份当前配置
save_config('config/backup_config.yaml')

# 加载特定配置文件
backup_config = load_config('config/backup_config.yaml')
```

## 📊 配置验证

### 自动验证

配置管理器提供自动验证功能：

```python
from tradingagents.config.config_manager import validate_config

# 验证当前配置
errors = validate_config()
if errors:
    print("配置错误:")
    for error in errors:
        print(f"  ❌ {error}")
else:
    print("✅ 配置验证通过")
```

### 验证规则

- **资金验证**: 初始资金必须大于0
- **股票池验证**: 股票池不能为空
- **经纪商验证**: 启用的经纪商必须有完整的凭证
- **邮件验证**: 启用邮件通知时必须配置收件人
- **端口验证**: Web端口必须在有效范围内

## 🔄 环境管理

### 多环境支持

```yaml
# 开发环境配置
environment: "development"

# 测试环境配置
environment: "testing"

# 生产环境配置
environment: "production"
```

### 环境特定配置

不同环境可以使用不同的配置：

```python
# 根据环境加载不同配置
import os

env = os.getenv('TRADING_ENV', 'development')
config_file = f'config/{env}_config.yaml'

config = load_config(config_file)
```

## 📚 最佳实践

### 1. 配置组织

- 将敏感信息（如API密钥）放在环境变量中
- 使用有意义的配置项名称和注释
- 为不同环境创建单独的配置文件

### 2. 安全建议

- 不要将API密钥和密码硬编码在配置文件中
- 使用环境变量或安全的密钥管理系统
- 定期轮换API凭证

### 3. 维护建议

- 定期备份配置文件
- 使用版本控制管理配置文件
- 记录配置变更历史

### 4. 调试技巧

- 使用 `validate_config()` 检查配置问题
- 查看日志了解配置加载情况
- 使用小步快跑的方式修改配置

## 🔍 故障排除

### 常见问题

#### Q: 配置加载失败

A: 检查配置文件语法是否正确，可以使用YAML验证工具检查格式。

#### Q: 模块无法读取配置

A: 确保已正确导入配置管理器，并检查配置项路径是否正确。

#### Q: 配置验证失败

A: 使用 `validate_config()` 函数查看具体错误信息。

#### Q: 热更新不生效

A: 某些配置可能需要重启相关模块才能生效。

## 🚀 高级用法

### 自定义配置类

```python
from tradingagents.config.config_manager import SystemConfig
from dataclasses import dataclass

@dataclass
class CustomConfig:
    custom_param: str = "default_value"

# 扩展系统配置
class ExtendedSystemConfig(SystemConfig):
    custom: CustomConfig = CustomConfig()
```

### 配置监听

```python
import threading

def config_watcher():
    """配置监控器"""
    last_modified = 0

    while True:
        try:
            # 检查配置文件修改时间
            current_modified = os.path.getmtime('tradingagents/config/user_config.yaml')

            if current_modified > last_modified:
                print("配置文件已修改，重新加载...")
                load_config()  # 重新加载配置
                last_modified = current_modified

            time.sleep(5)  # 每5秒检查一次

        except Exception as e:
            print(f"配置监控错误: {e}")
            time.sleep(5)

# 启动配置监控
watcher_thread = threading.Thread(target=config_watcher, daemon=True)
watcher_thread.start()
```

### 配置导出

```python
from tradingagents.config.config_manager import get_config
import json

# 导出配置为JSON
config = get_config()
config_dict = {
    'version': config.version,
    'trading': {
        'watchlist': config.trading.watchlist,
        'initial_cash': config.trading.initial_cash,
    },
    # ... 其他需要导出的配置
}

with open('exported_config.json', 'w', encoding='utf-8') as f:
    json.dump(config_dict, f, ensure_ascii=False, indent=2)

print("配置导出成功")
```

---

配置管理系统让TradingAgents更加灵活和易于维护。你可以根据不同的使用场景轻松调整各项参数，而无需修改代码。