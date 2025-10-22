# 🚀 TradingAgents 完整使用手册

## 目录

- [快速开始](#快速开始)
- [系统概述](#系统概述)
- [安装配置](#安装配置)
- [功能详解](#功能详解)
- [部署指南](#部署指南)
- [API参考](#api参考)
- [故障排除](#故障排除)
- [最佳实践](#最佳实践)
- [更新日志](#更新日志)

---

## 🚀 快速开始

### 一键启动

```bash
# 1. 克隆项目
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置系统
cp tradingagents/config/user_config_template.yaml tradingagents/config/user_config.yaml
nano tradingagents/config/user_config.yaml

# 4. 启动系统
python tradingagents/run.py
```

### 访问地址

- **现代化界面**: http://localhost:8501 (推荐)
- **传统界面**: http://localhost:5000
- **API文档**: http://localhost:8501 (内嵌)

---

## 📋 系统概述

### 核心特性

| 模块 | 功能 | 技术栈 | 就绪度 |
|------|------|--------|-------|
| 🤖 多智能体LLM | 个性化AI决策 | LangGraph + 多LLM | ✅ 完整 |
| 📊 高级技术分析 | 40+技术指标 | pandas-ta + talib | ✅ 完整 |
| ⏰ 自动化交易 | 定时任务 + 监控 | APScheduler | ✅ 完整 |
| 🌐 双前端界面 | Flask + Streamlit | Bootstrap + shadcn/ui | ✅ 完整 |
| 📧 邮件通知 | 多类型提醒 | smtplib + 模板 | ✅ 完整 |
| ⚙️ 配置管理 | 热更新 + 验证 | YAML + dataclass | ✅ 完整 |
| 🏦 经纪商集成 | 多平台API | RESTful + WebSocket | ✅ 完整 |
| 🛡️ 风险控制 | 多层防护 | 实时监控 + 熔断器 | ✅ 完整 |

### 智能体架构

```
分析师团队 (Analysts)
├── 市场分析师 (Market) → 技术指标分析
├── 基本面分析师 (Fundamentals) → 财务数据分析
├── 新闻分析师 (News) → 资讯影响评估
└── 社交媒体分析师 (Social) → 舆论情绪分析

研究员团队 (Researchers)
├── 看涨研究员 (Bull) → 优势论证
└── 看跌研究员 (Bear) → 风险辩驳

决策团队 (Decision)
├── 交易员 (Trader) → 综合决策
└── 风险管理 (Risk Manager) → 风险评估

数据层 (Data)
└── 多数据源集成 (Alpha Vantage, yfinance, Google News, Reddit)
```

---

## ⚙️ 安装配置

### 系统要求

- **Python**: 3.10+
- **内存**: 8GB+
- **存储**: 50GB+
- **网络**: 稳定的互联网连接

### 依赖包安装

```bash
# 核心依赖
pip install -r requirements.txt

# 前端界面依赖
pip install streamlit streamlit-shadcn-ui plotly

# 经纪商API依赖
pip install requests websocket-client

# 技术分析依赖
pip install pandas-ta talib-binary
```

### 配置文件设置

#### 1. 复制配置模板
```bash
cp tradingagents/config/user_config_template.yaml tradingagents/config/user_config.yaml
```

#### 2. 编辑关键配置

```yaml
# tradingagents/config/user_config.yaml
trading:
  watchlist:
    - "AAPL"        # 苹果
    - "GOOGL"       # 谷歌
    - "MSFT"        # 微软
    - "000858.SZ"   # 五粮液
  initial_cash: 100000.0

llm:
  researchers:
    provider: "openai"
    model: "o1-preview"
  analysts:
    provider: "openai"
    model: "gpt-4o"

broker:
  huatai:
    enabled: false  # 设为true启用真实交易
    app_key: "your_key"
    sandbox: true   # 生产环境设为false

email_notification:
  enabled: false
  email_user: "your_email@qq.com"
  recipients: ["user@example.com"]
```

---

## 🎯 功能详解

### 1. 多智能体LLM系统

#### 智能体分工

**分析师团队**:
- **市场分析师**: 技术指标分析、趋势识别
- **基本面分析师**: 财务数据分析、价值评估
- **新闻分析师**: 全球资讯分析、事件影响评估
- **社交媒体分析师**: 舆论情绪分析、热度追踪

**研究员团队**:
- **看涨研究员**: 挖掘投资机会、论证上涨逻辑
- **看跌研究员**: 识别潜在风险、论证下行理由

**决策团队**:
- **交易员**: 综合分析、制定交易策略
- **风险管理**: 评估风险、审核交易决策

#### LLM供应商分配

```python
# 不同智能体使用不同LLM
researchers: "o1-preview"      # 深度思考
analysts: "gpt-4o"             # 快速分析
trader: "gpt-4o"               # 平衡决策
risk_manager: "gpt-4o"         # 保守判断
```

### 2. 高级技术分析

#### 支持指标

**趋势指标**:
- 移动平均线 (SMA, EMA)
- MACD指标
- ADX趋势强度
- 布林带通道

**动量指标**:
- RSI相对强弱
- 随机指标KDJ
- Williams %R
- CCI顺势指标

**成交量指标**:
- OBV能量潮
- A/D累积分布线
- 成交量变化率

#### 使用示例

```python
from tradingagents.technical_analysis.advanced_indicators import AdvancedTechnicalAnalyzer

analyzer = AdvancedTechnicalAnalyzer()
result = analyzer.analyze_comprehensive(df, symbol='AAPL')

# 查看技术评分和信号
print(f"技术评分: {result['composite_score']:.2f}")
print(f"投资建议: {result['recommendation']}")
```

### 3. 自动化交易引擎

#### 定时任务

```python
# 市场分析（每30分钟）
scheduler.add_market_analysis_task(analysis_func, 30)

# 风险检查（每5分钟）
scheduler.add_portfolio_check_task(risk_check_func, 5)

# 每日报告（收盘后）
scheduler.add_daily_report_task(daily_report_func, "15:30")
```

#### 实时监控

- 价格异常波动检测
- 成交量放大监控
- 风险指标实时计算
- 持仓价值动态更新

### 4. 双前端界面

#### Streamlit现代化界面

```bash
# 启动现代化界面
python tradingagents/streamlit_app/run.py
# 访问: http://localhost:8501
```

**特性**:
- 🎨 shadcn/ui现代化组件
- 📊 实时数据看板
- 💹 交互式交易界面
- 🛡️ 可视化风险控制

#### Flask专业界面

```python
# 启动传统界面
from tradingagents.web_interface.app import run_web_server
run_web_server(host='localhost', port=5000)
# 访问: http://localhost:5000
```

**特性**:
- 📊 专业金融数据展示
- 💹 实时交易监控
- 🛡️ 企业级风险面板
- 📈 多周期技术图表

### 5. 经纪商API集成

#### 支持的经纪商

| 经纪商 | 状态 | 功能 |
|--------|------|------|
| 华泰证券 | ✅ 可用 | 完整交易API |
| 广发证券 | ✅ 可用 | 基础功能 |
| 中信证券 | 🚧 开发中 | 敬请期待 |

#### 使用示例

```python
from tradingagents.real_brokers.huatai_broker import HuataiBroker

config = {
    'app_key': 'your_app_key',
    'app_secret': 'your_app_secret',
    'account_id': 'your_account_id',
    'sandbox': True  # 生产环境设为False
}

broker = HuataiBroker(config)
await broker.connect()
account = await broker.get_account_info()
```

---

## 🚀 部署指南

### 开发环境部署

```bash
# 1. 启动后端服务
python -m tradingagents.automated_trading

# 2. 启动前端界面（选择其一）
# 现代化界面
python tradingagents/streamlit_app/run.py

# 或传统界面
python -m tradingagents.web_interface.app
```

### 生产环境部署

#### Docker部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python setup.py install

EXPOSE 8501 5000
CMD ["python", "tradingagents/run.py"]
```

```bash
# 构建和运行
docker build -t tradingagents .
docker run -d -p 8501:8501 -p 5000:5000 --name tradingagents tradingagents
```

#### 系统服务部署

```bash
# 创建系统服务
sudo cp scripts/tradingagents.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tradingagents
sudo systemctl start tradingagents

# 查看服务状态
sudo systemctl status tradingagents
```

### 监控和运维

#### 健康检查

```bash
# 检查系统健康
curl http://localhost:8501/api/health

# 检查交易状态
curl http://localhost:8501/api/status
```

#### 日志监控

```bash
# 查看实时日志
tail -f logs/tradingagents.log

# 查看错误日志
grep ERROR logs/tradingagents.log
```

---

## 🔧 API参考

### 配置管理API

```python
from tradingagents.config.config_manager import get_config, update_config, validate_config

# 获取配置
config = get_config()

# 更新配置
update_config({
    'trading': {'analysis_interval': 15},
    'llm': {'analysts': {'model': 'gpt-4o-mini'}}
})

# 验证配置
errors = validate_config()
```

### 多智能体LLM API

```python
from tradingagents.llm.llm_factory import get_llm_for_agent, get_llm_performance_report

# 获取智能体LLM
analyst_llm = get_llm_for_agent('market_analyst')

# 查看性能报告
report = get_llm_performance_report()
print(f"总成本: ${report['cost_summary']['total_cost']}")
```

### 自动化交易API

```python
from tradingagents.automated_trading import AutomatedTrader, TradingConfig

# 创建交易配置
config = TradingConfig(
    watchlist=['AAPL', 'GOOGL'],
    initial_cash=100000.0
)

# 创建交易器
trader = AutomatedTrader(config)
trader.start()  # 启动自动交易
```

### 经纪商API

```python
from tradingagents.real_brokers.huatai_broker import HuataiBroker

# 配置经纪商
broker = HuataiBroker({
    'app_key': 'your_key',
    'sandbox': True
})

# 连接并交易
await broker.connect()
await broker.authenticate()

# 下单
order_id = await broker.place_order(
    symbol='AAPL',
    quantity=100,
    side='buy',
    order_type='market'
)
```

---

## 🛠️ 故障排除

### 常见问题

#### Q: 配置加载失败
```bash
# 检查配置语法
python -c "import yaml; yaml.safe_load(open('tradingagents/config/user_config.yaml'))"

# 验证配置
python -c "from tradingagents.config.config_manager import validate_config; print(validate_config())"
```

#### Q: LLM服务连接失败
```bash
# 检查API密钥
python -c "import os; print('OPENAI_API_KEY' in os.environ)"

# 测试LLM连接
python -c "from tradingagents.llm.llm_factory import llm_factory; print(llm_factory.health_check())"
```

#### Q: 前端界面无法访问
```bash
# 检查端口占用
netstat -tlnp | grep :8501
netstat -tlnp | grep :5000

# 重启前端服务
pkill -f streamlit
pkill -f "python.*web_interface"
```

#### Q: 交易数据不更新
```bash
# 检查WebSocket连接
curl http://localhost:8501/api/status

# 重启自动化交易引擎
python -c "from tradingagents.automated_trading import automated_trader; automated_trader.stop(); automated_trader.start()"
```

### 调试技巧

#### 日志级别设置

```python
import logging

# 设置详细日志
logging.getLogger('tradingagents').setLevel(logging.DEBUG)

# 查看特定模块日志
logging.getLogger('tradingagents.llm').setLevel(logging.DEBUG)
```

#### 性能分析

```python
import cProfile

# 性能分析
profiler = cProfile.Profile()
profiler.enable()

# 运行代码
your_code_here()

profiler.disable()
profiler.print_stats(sort='cumulative')
```

---

## 📚 最佳实践

### 1. 配置管理最佳实践

```yaml
# 生产环境配置示例
environment: "production"

trading:
  analysis_interval: 15      # 更频繁的分析
  risk_check_interval: 3     # 更密集的风险检查

risk_management:
  max_portfolio_risk: 0.15   # 更保守的风险控制
  stop_loss_ratio: 0.05      # 较紧的止损

logging:
  level: "WARNING"           # 生产环境减少日志
  enable_console: false      # 禁用控制台输出
```

### 2. 多LLM分配策略

```yaml
# 成本效益最优配置
llm:
  market_analyst:
    model: "gpt-4o-mini"     # 成本最优
  fundamentals_analyst:
    model: "gpt-4o"          # 平衡成本质量
  bull_researcher:
    model: "o1-preview"      # 最高质量
```

### 3. 风险控制最佳实践

```yaml
# 多层风险控制
risk_management:
  max_position_per_stock: 10000.0    # 单股限额
  max_portfolio_risk: 0.2            # 组合风险
  max_daily_loss: 0.03               # 单日止损
  enable_dynamic_stop_loss: true      # 动态止损
  enable_trailing_stop: true         # 追踪止损
```

### 4. 监控和运维最佳实践

```bash
# 定期健康检查
*/5 * * * * curl -f http://localhost:8501/api/health || systemctl restart tradingagents

# 定期备份配置
0 2 * * * cp tradingagents/config/user_config.yaml backups/config_$(date +%Y%m%d_%H%M%S).yaml

# 定期清理日志
0 3 * * * find logs/ -name "*.log" -size +100M -delete
```

---

## 🔄 更新日志

### v2.0.0 (最新版) - 多智能体LLM供应商系统

#### 🚀 新增功能
- ✅ 多智能体个性化LLM配置
- ✅ Streamlit现代化前端界面
- ✅ 完整经纪商API集成
- ✅ 高级技术分析工具库
- ✅ 统一配置管理系统
- ✅ 企业级监控和熔断器

#### 🔧 改进优化
- 📈 提升多智能体协作效率
- 🛡️ 加强风险控制机制
- 📊 优化数据可视化效果
- ⚙️ 完善配置管理功能

#### 🐛 修复问题
- 修复LLM实例缓存问题
- 优化内存使用效率
- 改进错误处理机制

### v1.5.0 - 自动化交易引擎

#### 🚀 新增功能
- ⏰ 定时任务调度系统
- 📊 实时市场监控器
- 💼 模拟交易接口
- 📧 邮件通知服务

### v1.0.0 - 核心多智能体系统

#### 🚀 初始版本
- 🤖 多智能体LLM交易决策
- 📈 基础技术分析
- 🌐 Web管理界面
- ⚙️ 基础配置系统

---

## 📞 技术支持

### 获取帮助

1. **文档中心**: 查看本文档和各模块README
2. **示例程序**: 运行各种示例程序熟悉功能
3. **社区论坛**: 访问项目GitHub讨论区
4. **技术支持**: 发送邮件至 support@tradingagents.ai

### 报告问题

请提供以下信息：
- TradingAgents版本号
- Python版本和操作系统
- 详细错误信息和复现步骤
- 相关配置文件（脱敏处理）

### 贡献代码

欢迎社区贡献：
1. Fork项目仓库
2. 创建功能分支
3. 提交Pull Request
4. 参与代码审查

---

**免责声明**: 本系统仅供学习和研究使用。请勿用于实际交易，所有交易操作需自行承担风险和责任。使用前请仔细阅读相关法律法规要求。

---

*TradingAgents - 开启智能交易新时代* 🚀