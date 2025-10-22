# 🤖 TradingAgents 多智能体LLM供应商系统

## 概述

TradingAgents 的多智能体LLM供应商系统允许为不同的智能体分配不同的LLM供应商和模型，实现最优的性能和成本平衡。

## 🎯 核心特性

### ✅ 多供应商支持
- **OpenAI**: GPT-4, GPT-3.5, o1-preview 等模型
- **Anthropic**: Claude-3 系列模型
- **Google**: Gemini 系列模型
- **本地部署**: Ollama, vLLM 等
- **第三方**: OpenRouter, Together AI 等

### ✅ 智能体个性化配置
- **研究员**: 使用深度思考模型 (o1-preview)
- **分析师**: 使用快速分析模型 (gpt-4o)
- **交易员**: 使用平衡决策模型 (gpt-4o)
- **风险管理**: 使用保守决策模型 (gpt-4o)

### ✅ 企业级特性
- **性能监控**: 实时监控LLM使用情况和响应时间
- **成本控制**: 精确计算和控制LLM使用成本
- **熔断器保护**: 防止故障扩散的保护机制
- **健康检查**: 自动检测和报告LLM健康状态

## 📁 系统架构

```
tradingagents/llm/
├── __init__.py              # 模块入口
├── llm_factory.py           # LLM工厂核心类 (443行)
└── README.md               # 本文档

配置系统:
├── config/config_manager.py # 配置管理器
├── config/default_config.yaml # 默认配置
└── config/user_config_template.yaml # 用户模板
```

## 🚀 快速开始

### 1. 配置多LLM供应商

```yaml
# user_config.yaml
llm:
  # 研究员使用深度思考模型
  researchers:
    provider: "openai"
    model: "o1-preview"
    temperature: 0.8
    max_tokens: 4096

  # 分析师使用快速模型
  analysts:
    provider: "openai"
    model: "gpt-4o"
    temperature: 0.3
    max_tokens: 2048

  # 风险管理使用保守设置
  risk_manager:
    provider: "openai"
    model: "gpt-4o"
    temperature: 0.1
    max_tokens: 2048
```

### 2. 在代码中使用

```python
from tradingagents.llm.llm_factory import get_llm_for_agent

# 为市场分析师获取LLM
market_llm = get_llm_for_agent('market_analyst')

# 为研究员获取LLM
researcher_llm = get_llm_for_agent('bull_researcher')

# 为风险管理获取LLM
risk_llm = get_llm_for_agent('risk_manager')
```

### 3. 记录使用情况

```python
from tradingagents.llm.llm_factory import record_llm_usage

# 记录成功请求
record_llm_usage('market_analyst', True, 1.2, 150)

# 记录失败请求
record_llm_usage('market_analyst', False, 0.0, 0)
```

## 📊 智能体最优配置推荐

### 🎓 研究员 (Researchers)
```yaml
researchers:
  provider: "openai"
  model: "o1-preview"        # 深度思考能力强
  temperature: 0.8          # 较高创造性
  max_tokens: 4096          # 支持长文本分析
  timeout: 60               # 允许更长思考时间
```

**适用场景**: 市场研究、趋势分析、投资策略制定

### 📈 分析师 (Analysts)
```yaml
analysts:
  provider: "openai"
  model: "gpt-4o"           # 快速准确
  temperature: 0.3          # 保守分析
  max_tokens: 2048          # 适中响应长度
  timeout: 25               # 快速响应
```

**适用场景**: 技术分析、基本面分析、实时数据处理

### 💼 交易员 (Trader)
```yaml
trader:
  provider: "openai"
  model: "gpt-4o"           # 平衡决策
  temperature: 0.2          # 谨慎决策
  max_tokens: 2048          # 清晰指令
  timeout: 25
```

**适用场景**: 交易决策、时机把握、仓位管理

### 🛡️ 风险管理 (Risk Manager)
```yaml
risk_manager:
  provider: "openai"
  model: "gpt-4o"           # 稳定可靠
  temperature: 0.1          # 非常保守
  max_tokens: 2048          # 精确计算
  timeout: 25
```

**适用场景**: 风险评估、止损设置、合规检查

## 🔧 高级配置

### 多供应商配置示例

```yaml
llm:
  # OpenAI 配置
  analysts:
    provider: "openai"
    model: "gpt-4o"
    backend_url: "https://api.openai.com/v1"

  # Anthropic 配置
  researchers:
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    backend_url: "https://api.anthropic.com"

  # Google 配置
  risk_manager:
    provider: "google"
    model: "gemini-pro"

  # 本地部署配置
  trader:
    provider: "ollama"
    model: "llama2:13b"
    backend_url: "http://localhost:11434"
```

### 成本优化配置

```yaml
llm:
  # 高频分析师用成本优化的模型
  market_analyst:
    provider: "openai"
    model: "gpt-4o-mini"     # 成本最低的GPT模型
    temperature: 0.4
    max_tokens: 2048

  # 深度分析用高质量模型
  fundamentals_analyst:
    provider: "openai"
    model: "gpt-4o"          # 质量与成本平衡
    temperature: 0.3
    max_tokens: 2048

  # 研究任务用最优模型
  bull_researcher:
    provider: "openai"
    model: "o1-preview"      # 最高质量，较高成本
    temperature: 0.7
    max_tokens: 4096
```

## 📊 监控和分析

### 性能监控

```python
from tradingagents.llm.llm_factory import get_llm_performance_report

# 获取性能报告
report = get_llm_performance_report()

print(f"总成本: ${report['cost_summary']['total_cost']:.3f}")
print(f"总token数: {report['cost_summary']['total_tokens']:,}")

# 按智能体查看性能
for agent, stats in report['performance_by_agent'].items():
    print(f"{agent}: 成功率 {stats['success_rate']:.1%}, 成本 ${stats['total_cost']:.3f}")
```

### 健康检查

```python
from tradingagents.llm.llm_factory import get_llm_health_report

# 获取健康报告
health = get_llm_health_report()

print(f"整体健康状态: {health['overall_health']}")

if health['unhealthy_agents']:
    print("需要关注的智能体:")
    for item in health['unhealthy_agents']:
        print(f"  - {item['agent']}: 健康评分 {item['health_score']:.2f}")
```

### LLM映射查看

```python
from tradingagents.llm.llm_factory import get_agent_llm_mapping

# 查看智能体LLM配置
mapping = get_agent_llm_mapping()

for agent_type, config in mapping.items():
    print(f"{agent_type}: {config['provider']}/{config['model']}")
```

## 💰 成本管理

### 成本估算

系统内置多种模型的成本估算：

| 模型 | 成本 (每1000 tokens) | 推荐用途 |
|------|---------------------|----------|
| gpt-4o | $0.03 | 高质量分析 |
| gpt-4o-mini | $0.0015 | 快速分析 |
| o1-preview | $0.15 | 深度研究 |
| Claude-3-5-Sonnet | $0.03 | 平衡使用 |

### 成本控制策略

```yaml
llm:
  # 为不同智能体设置不同的成本控制
  market_analyst:
    max_requests_per_minute: 30    # 限制请求频率
    max_tokens: 1024              # 限制响应长度

  bull_researcher:
    max_requests_per_minute: 10    # 研究任务较少
    max_tokens: 4096              # 需要详细分析
```

## 🔧 故障处理

### 熔断器机制

系统内置熔断器保护：

```python
# 熔断器配置示例
circuit_breaker:
  failure_threshold: 5      # 连续失败5次触发熔断
  recovery_timeout: 60      # 熔断60秒后恢复
```

### 自动故障转移

```python
# 当主LLM故障时，自动切换到备用配置
fallback_config = {
  'backup_llm': {
    'provider': 'openai',
    'model': 'gpt-4o-mini',     # 备用模型
    'temperature': 0.3
  }
}
```

## 🚀 使用示例

### 基本使用

```python
# 运行多LLM示例程序
python tradingagents/multi_llm_example.py
```

### 在自动化交易中使用

```python
from tradingagents.automated_trading import AutomatedTrader
from tradingagents.llm.llm_factory import get_llm_for_agent

# 创建自动化交易器（会自动使用多LLM配置）
trader = AutomatedTrader()

# 手动获取特定智能体的LLM
analyst_llm = get_llm_for_agent('market_analyst')
researcher_llm = get_llm_for_agent('bull_researcher')

# 查看LLM映射
mapping = get_agent_llm_mapping()
print("智能体LLM配置:", mapping)
```

### 性能监控集成

```python
import time
from tradingagents.llm.llm_factory import get_llm_for_agent, record_llm_usage

# 使用LLM并记录性能
start_time = time.time()
llm = get_llm_for_agent('market_analyst')

try:
    # 执行LLM任务
    response = llm.invoke("分析市场趋势...")
    response_time = time.time() - start_time

    # 记录成功使用
    tokens_used = len(response.content.split()) * 1.3  # 估算token数
    record_llm_usage('market_analyst', True, response_time, int(tokens_used))

except Exception as e:
    # 记录失败使用
    record_llm_usage('market_analyst', False, time.time() - start_time, 0)
```

## 📈 性能优化建议

### 1. 模型选择优化

- **研究员**: o1-preview → 深度思考，高质量研究
- **分析师**: gpt-4o-mini → 快速响应，成本优化
- **交易员**: gpt-4o → 平衡质量和速度
- **风险管理**: gpt-4o → 稳定可靠，保守决策

### 2. 参数调优

- **温度设置**: 研究员 0.7-0.8，分析师 0.3-0.4，风险管理 0.1-0.2
- **Token限制**: 根据任务复杂度设置合适的响应长度
- **超时设置**: 深度思考任务可设置更长超时时间

### 3. 成本控制

- 监控各智能体的实际使用成本
- 根据任务重要性分配不同质量的模型
- 设置成本预警和限制机制

## 🔍 故障排除

### 常见问题

#### Q: LLM响应质量不稳定
A: 调整温度参数，或切换到更稳定的模型。

#### Q: 成本超出预期
A: 检查各智能体的实际使用情况，优化模型选择。

#### Q: 响应时间过长
A: 降低max_tokens或切换到更快模型。

#### Q: 某个智能体频繁失败
A: 检查熔断器状态，可能需要调整失败阈值。

## 🚀 下一步扩展

### 支持更多供应商
- [ ] 本地模型部署 (vLLM, Ollama)
- [ ] 企业级API (Azure OpenAI)
- [ ] 其他供应商 (Together AI, Replicate)

### 高级功能
- [ ] 动态模型切换
- [ ] 智能成本优化
- [ ] 多模型投票机制
- [ ] 模型蒸馏和压缩

---

多智能体多LLM供应商系统让TradingAgents能够充分利用不同AI模型的优势，为各类任务选择最合适的AI助手，实现性能和成本的最优平衡。