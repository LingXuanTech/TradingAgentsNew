"""
多智能体LLM供应商模块
为不同智能体提供个性化的LLM供应商支持
"""

from .llm_factory import (
    LLMFactory,
    LLMPerformanceMetrics,
    LLMCircuitBreaker,
    get_llm_for_agent,
    record_llm_usage,
    get_llm_performance_report,
    get_llm_health_report,
    get_agent_llm_mapping
)

# 全局LLM工厂实例
from .llm_factory import llm_factory

__version__ = "1.0.0"

__all__ = [
    # 核心类
    "LLMFactory",
    "LLMPerformanceMetrics",
    "LLMCircuitBreaker",

    # 便捷函数
    "get_llm_for_agent",
    "record_llm_usage",
    "get_llm_performance_report",
    "get_llm_health_report",
    "get_agent_llm_mapping",

    # 全局实例
    "llm_factory",
]