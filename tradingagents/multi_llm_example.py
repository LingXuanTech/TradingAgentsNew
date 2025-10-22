#!/usr/bin/env python3
"""
多智能体多LLM供应商使用示例
展示如何为不同智能体分配不同的LLM供应商和模型
"""

import time
import logging
from typing import Dict, Any

# 导入多LLM系统
from tradingagents.llm.llm_factory import (
    LLMFactory, get_llm_for_agent, record_llm_usage,
    get_llm_performance_report, get_llm_health_report, get_agent_llm_mapping
)

# 导入配置管理器
from tradingagents.config.config_manager import get_config, update_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demonstrate_llm_factory():
    """演示LLM工厂功能"""
    print("=" * 60)
    print("🏭 多智能体LLM工厂演示")
    print("=" * 60)

    # 创建LLM工厂
    llm_factory = LLMFactory()

    print("📋 LLM工厂功能:")
    print("   ✅ 多供应商支持: OpenAI, Anthropic, Google")
    print("   ✅ 智能体个性化配置: 为每个智能体定制LLM参数")
    print("   ✅ 性能监控: 实时监控LLM使用情况和成本")
    print("   ✅ 熔断器保护: 防止故障扩散")
    print("   ✅ 成本控制: 精确计算和控制LLM使用成本")

    # 显示智能体LLM映射
    print("\n🗺️  智能体LLM映射:")
    mapping = get_agent_llm_mapping()
    for agent_type, config in mapping.items():
        print(f"   - {agent_type}: {config['provider']}/{config['model']} (temp: {config['temperature']})")

    return llm_factory


def demonstrate_agent_llm_usage():
    """演示智能体LLM使用"""
    print("\n" + "=" * 60)
    print("🤖 智能体个性化LLM演示")
    print("=" * 60)

    # 测试不同智能体的LLM实例
    agent_types = [
        'market_analyst',
        'bull_researcher',
        'trader',
        'risk_manager'
    ]

    print("🔧 为不同智能体获取个性化LLM:")

    for agent_type in agent_types:
        try:
            llm = get_llm_for_agent(agent_type)

            # 获取LLM配置信息
            mapping = get_agent_llm_mapping()
            config = mapping[agent_type]

            print(f"   ✅ {agent_type}:")
            print(f"      - 供应商/模型: {config['provider']}/{config['model']}")
            print(f"      - 温度参数: {config['temperature']}")
            print(f"      - 最大token: {config['max_tokens']}")
            print(f"      - LLM实例: {type(llm).__name__}")

        except Exception as e:
            print(f"   ❌ {agent_type}: 获取LLM失败 - {str(e)}")

    return True


def demonstrate_performance_monitoring():
    """演示性能监控功能"""
    print("\n" + "=" * 60)
    print("📊 LLM性能监控演示")
    print("=" * 60)

    # 模拟一些LLM使用记录
    print("📈 模拟LLM使用情况...")

    # 模拟成功请求
    record_llm_usage('market_analyst', True, 1.2, 150)
    record_llm_usage('bull_researcher', True, 3.5, 800)
    record_llm_usage('trader', True, 0.8, 200)
    record_llm_usage('risk_manager', True, 0.9, 180)

    # 模拟失败请求
    record_llm_usage('market_analyst', False, 0.0, 0)

    # 获取性能报告
    performance_report = get_llm_performance_report()

    print("📋 性能报告:")
    print(f"   - 服务智能体数: {performance_report['total_agents']}")
    print(f"   - LLM实例数: {performance_report['total_llm_instances']}")
    print(f"   - 总成本: ${performance_report['cost_summary']['total_cost']:.3f}")
    print(f"   - 总token数: {performance_report['cost_summary']['total_tokens']:,}")

    # 按智能体显示性能
    print("\n🏢 按智能体性能统计:")
    for agent, stats in performance_report['performance_by_agent'].items():
        print(f"   - {agent}:")
        print(f"     请求数: {stats['total_requests']}")
        print(f"     成功率: {stats['success_rate']:.1%}")
        print(f"     平均响应时间: {stats['avg_response_time']:.2f}秒")
        print(f"     成本: ${stats['total_cost']:.3f}")


def demonstrate_health_monitoring():
    """演示健康监控功能"""
    print("\n" + "=" * 60)
    print("❤️ LLM健康监控演示")
    print("=" * 60)

    # 获取健康报告
    health_report = get_llm_health_report()

    print("🏥 系统健康状态:")
    print(f"   - 整体状态: {health_report['overall_health']}")

    print("
✅ 健康智能体:"    for agent in health_report['healthy_agents']:
        print(f"   - {agent}")

    if health_report['unhealthy_agents']:
        print("
⚠️  不健康智能体:"        for item in health_report['unhealthy_agents']:
            print(f"   - {item['agent']}: 健康评分 {item['health_score']:.2f}")

    if health_report['circuit_breaker_trips']:
        print("
🔥 熔断器触发:"        for item in health_report['circuit_breaker_trips']:
            print(f"   - {item['agent']}: 失败 {item['failure_count']} 次")


def demonstrate_llm_cost_analysis():
    """演示LLM成本分析"""
    print("\n" + "=" * 60)
    print("💰 LLM成本分析演示")
    print("=" * 60)

    # 获取LLM工厂实例
    llm_factory = LLMFactory()

    # 显示成本估算配置
    print("💵 成本估算配置 (每1000 tokens):")
    for model, cost in llm_factory.cost_per_1k_tokens.items():
        print(f"   - {model}: ${cost}")

    # 显示成本汇总
    cost_summary = llm_factory.get_llm_cost_summary()
    print("
📊 成本汇总:"    print(f"   - 总成本: ${cost_summary['total_cost']:.3f}")
    print(f"   - 总token数: {cost_summary['total_cost']:,}")

    print("
📈 按供应商成本:"    for provider, cost in cost_summary['cost_by_provider'].items():
        print(f"   - {provider}: ${cost:.3f}")

    print("
👥 按智能体成本:"    for agent, cost in cost_summary['cost_by_agent'].items():
        print(f"   - {agent}: ${cost:.3f}")


def demonstrate_config_based_llm():
    """演示基于配置的LLM管理"""
    print("\n" + "=" * 60)
    print("⚙️ 基于配置的LLM管理演示")
    print("=" * 60)

    # 显示当前配置
    config = get_config()
    print("📋 当前LLM配置:")

    # 显示研究员配置
    researcher_config = config.llm['researchers']
    print(f"   - 研究员: {researcher_config.provider}/{researcher_config.model}")
    print(f"     温度: {researcher_config.temperature}")
    print(f"     最大token: {researcher_config.max_tokens}")

    # 显示分析师配置
    analyst_config = config.llm['analysts']
    print(f"   - 分析师: {analyst_config.provider}/{analyst_config.model}")
    print(f"     温度: {analyst_config.temperature}")
    print(f"     最大token: {analyst_config.max_tokens}")

    # 演示配置更新
    print("
🔄 配置更新演示:"    print("   - 更新研究员使用Claude-3...")

    # 更新配置示例
    new_llm_config = {
        'llm': {
            'researchers': {
                'provider': 'anthropic',
                'model': 'claude-3-5-sonnet',
                'temperature': 0.7,
                'max_tokens': 4096
            }
        }
    }

    print("   - 新配置已准备，实际部署时会调用 update_config()")


def demonstrate_llm_comparison():
    """演示不同LLM供应商对比"""
    print("\n" + "=" * 60)
    print("⚖️ LLM供应商对比演示")
    print("=" * 60)

    print("🏆 供应商推荐配置:")

    # 成本效益分析
    print("
💡 成本效益推荐:"    print("   - 高质量分析: gpt-4o (平衡成本和质量)")
    print("   - 深度思考: o1-preview (高质量研究)")
    print("   - 快速响应: gpt-4o-mini (成本最优)")
    print("   - 保守决策: gpt-4o (稳定可靠)")

    # 智能体最优配置建议
    print("
🎯 智能体最优配置:"    print("   - 研究员: o1-preview (深度思考)")
    print("   - 分析师: gpt-4o (快速准确)")
    print("   - 交易员: gpt-4o (平衡决策)")
    print("   - 风险管理: gpt-4o (保守稳定)")

    # 成本对比
    print("
💰 成本对比 (估算):"    print("   - gpt-4o: $0.03/1K tokens")
    print("   - gpt-4o-mini: $0.0015/1K tokens")
    print("   - o1-preview: $0.15/1K tokens")
    print("   - Claude-3-5-Sonnet: $0.03/1K tokens")


def demonstrate_error_handling():
    """演示错误处理机制"""
    print("\n" + "=" * 60)
    print("🛡️ 错误处理机制演示")
    print("=" * 60)

    print("🔧 错误处理功能:")
    print("   ✅ 熔断器保护: 连续失败时自动熔断")
    print("   ✅ 自动重试: 可配置的重试机制")
    print("   ✅ 故障转移: 自动切换到备用LLM")
    print("   ✅ 性能监控: 实时监控LLM健康状态")
    print("   ✅ 成本控制: 防止意外的大额支出")

    # 演示熔断器逻辑
    print("
🔥 熔断器示例:"    print("   - 连续失败5次 → 触发熔断")
    print("   - 熔断期间60秒 → 使用备用配置")
    print("   - 自动恢复 → 故障排除后恢复正常")

    # 演示成本控制
    print("
💰 成本控制示例:"    print("   - 单次请求成本估算")
    print("   - 每日成本限制")
    print("   - 异常成本预警")


def main():
    """主函数"""
    print("🚀 TradingAgents 多智能体多LLM供应商系统演示")
    print("展示为不同智能体分配不同LLM供应商的完整解决方案")

    try:
        # LLM工厂演示
        llm_factory = demonstrate_llm_factory()

        # 智能体LLM使用演示
        demonstrate_agent_llm_usage()

        # 性能监控演示
        demonstrate_performance_monitoring()

        # 健康监控演示
        demonstrate_health_monitoring()

        # 成本分析演示
        demonstrate_llm_cost_analysis()

        # 基于配置的LLM管理演示
        demonstrate_config_based_llm()

        # LLM供应商对比演示
        demonstrate_llm_comparison()

        # 错误处理演示
        demonstrate_error_handling()

        print("\n" + "=" * 60)
        print("🎉 多LLM供应商系统演示完成！")
        print("=" * 60)

        print("\n🌟 系统优势:")
        print("   ✅ 个性化配置: 每个智能体都有最适合的LLM")
        print("   ✅ 成本优化: 根据任务复杂度选择性价比最优的模型")
        print("   ✅ 性能监控: 实时监控LLM使用情况和健康状态")
        print("   ✅ 故障保护: 熔断器和自动恢复机制")
        print("   ✅ 灵活扩展: 轻松添加新的供应商和智能体类型")

        print("\n📚 使用建议:")
        print("   1. 根据实际需求调整各智能体的LLM配置")
        print("   2. 监控成本使用情况，避免意外支出")
        print("   3. 利用健康检查功能及时发现问题")
        print("   4. 根据性能数据优化智能体LLM分配")

        print("\n🔗 相关资源:")
        print("   - 配置管理: tradingagents/config/README.md")
        print("   - LLM工厂文档: 各函数的docstring")
        print("   - 性能监控API: get_llm_performance_report()")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        logger.exception("演示错误详情")


if __name__ == "__main__":
    main()