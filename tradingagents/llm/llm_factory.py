"""
多智能体LLM工厂系统
为不同智能体提供个性化的LLM供应商支持
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 导入配置管理器
from ..config.config_manager import get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMPerformanceMetrics:
    """LLM性能指标"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    average_response_time: float = 0.0
    last_request_time: Optional[datetime] = None
    error_count: int = 0
    consecutive_failures: int = 0

    # 成本统计
    total_tokens: int = 0
    total_cost: float = 0.0

    def update_success(self, response_time: float, tokens: int = 0, cost: float = 0.0):
        """更新成功请求指标"""
        self.total_requests += 1
        self.successful_requests += 1
        self.total_response_time += response_time
        self.average_response_time = self.total_response_time / self.total_requests
        self.last_request_time = datetime.now()
        self.consecutive_failures = 0

        if tokens > 0:
            self.total_tokens += tokens
        if cost > 0:
            self.total_cost += cost

    def update_failure(self):
        """更新失败请求指标"""
        self.total_requests += 1
        self.failed_requests += 1
        self.consecutive_failures += 1
        self.error_count += 1

    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    def get_health_score(self) -> float:
        """获取健康评分 (0-1)"""
        if self.total_requests == 0:
            return 1.0

        # 基于成功率、响应时间和连续失败次数计算健康评分
        success_score = self.get_success_rate()
        failure_penalty = min(0.3, self.consecutive_failures * 0.1)
        time_penalty = min(0.2, (self.average_response_time / 10.0) * 0.1)

        return max(0.0, success_score - failure_penalty - time_penalty)


@dataclass
class LLMCircuitBreaker:
    """LLM熔断器"""
    failure_threshold: int = 5
    recovery_timeout: int = 60  # 秒
    failure_timestamps: deque = field(default_factory=deque)

    def can_proceed(self) -> bool:
        """检查是否可以继续请求"""
        now = time.time()

        # 移除过期的失败记录
        while self.failure_timestamps and now - self.failure_timestamps[0] > self.recovery_timeout:
            self.failure_timestamps.popleft()

        return len(self.failure_timestamps) < self.failure_threshold

    def record_failure(self):
        """记录失败"""
        self.failure_timestamps.append(time.time())

    def get_failure_count(self) -> int:
        """获取当前失败次数"""
        return len(self.failure_timestamps)


class LLMFactory:
    """LLM工厂 - 集中式多供应商管理"""

    def __init__(self):
        """初始化LLM工厂"""
        self.config = get_config()
        self.llm_instances: Dict[str, Any] = {}  # 缓存LLM实例
        self.performance_metrics: Dict[str, LLMPerformanceMetrics] = {}
        self.circuit_breakers: Dict[str, LLMCircuitBreaker] = {}
        self._lock = threading.Lock()

        # 支持的供应商映射
        self.provider_classes = {
            'openai': ChatOpenAI,
            'anthropic': ChatAnthropic,
            'google': ChatGoogleGenerativeAI,
        }

        # 成本估算配置（每1000tokens的美元成本）
        self.cost_per_1k_tokens = {
            'gpt-4o': 0.03,
            'gpt-4o-mini': 0.0015,
            'o1-preview': 0.15,
            'claude-3-5-sonnet': 0.03,
            'claude-3-haiku': 0.0025,
            'gemini-pro': 0.0025,
        }

        logger.info("LLM工厂初始化完成")

    def get_llm_for_agent(self, agent_type: str) -> Any:
        """
        为指定智能体获取对应的LLM实例

        Args:
            agent_type: 智能体类型，如 'market_analyst', 'bull_researcher' 等

        Returns:
            配置好的LLM实例
        """
        # 获取智能体配置
        agent_config = self._get_agent_llm_config(agent_type)

        # 检查熔断器
        if not self._check_circuit_breaker(agent_type):
            logger.warning(f"智能体 {agent_type} LLM熔断器激活，使用备用配置")
            # 使用默认配置作为备用
            agent_config = self.config.llm.get('default', self.config.llm['analysts'])

        # 获取或创建LLM实例
        llm_key = self._get_llm_key(agent_type, agent_config)

        with self._lock:
            if llm_key not in self.llm_instances:
                self.llm_instances[llm_key] = self._create_llm_instance(agent_config)
                self.performance_metrics[llm_key] = LLMPerformanceMetrics()
                self.circuit_breakers[llm_key] = LLMCircuitBreaker()

        return self.llm_instances[llm_key]

    def _get_agent_llm_config(self, agent_type: str):
        """获取智能体LLM配置"""
        # 智能体类型到配置的映射
        agent_config_map = {
            # 分析师
            'market_analyst': self.config.llm.get('market_analyst', self.config.llm['analysts']),
            'fundamentals_analyst': self.config.llm.get('fundamentals_analyst', self.config.llm['analysts']),
            'news_analyst': self.config.llm.get('news_analyst', self.config.llm['analysts']),
            'social_media_analyst': self.config.llm.get('social_media_analyst', self.config.llm['analysts']),

            # 研究员
            'bull_researcher': self.config.llm.get('bull_researcher', self.config.llm['researchers']),
            'bear_researcher': self.config.llm.get('bear_researcher', self.config.llm['researchers']),

            # 经理
            'research_manager': self.config.llm.get('research_manager', self.config.llm['researchers']),
            'risk_judge': self.config.llm.get('risk_judge', self.config.llm['risk_manager']),

            # 风险分析师
            'risky_analyst': self.config.llm.get('risky_analyst', self.config.llm['risk_manager']),
            'safe_analyst': self.config.llm.get('safe_analyst', self.config.llm['risk_manager']),
            'neutral_analyst': self.config.llm.get('neutral_analyst', self.config.llm['risk_manager']),

            # 交易员
            'trader': self.config.llm.get('trader', self.config.llm['default']),
        }

        # 返回对应配置，如果没有找到则使用默认配置
        return agent_config_map.get(agent_type, self.config.llm['default'])

    def _create_llm_instance(self, agent_config) -> Any:
        """创建LLM实例"""
        try:
            provider = agent_config.provider.lower()
            model = agent_config.model

            if provider not in self.provider_classes:
                raise ValueError(f"不支持的LLM供应商: {provider}")

            # 根据供应商创建对应实例
            if provider == 'openai':
                llm = ChatOpenAI(
                    model=model,
                    base_url=agent_config.backend_url,
                    temperature=agent_config.temperature,
                    max_tokens=agent_config.max_tokens,
                    top_p=agent_config.top_p,
                    frequency_penalty=agent_config.frequency_penalty,
                    presence_penalty=agent_config.presence_penalty,
                    timeout=agent_config.timeout,
                    max_retries=agent_config.max_retries
                )

            elif provider == 'anthropic':
                llm = ChatAnthropic(
                    model=model,
                    base_url=agent_config.backend_url,
                    temperature=agent_config.temperature,
                    max_tokens=agent_config.max_tokens,
                    timeout=agent_config.timeout,
                    max_retries=agent_config.max_retries
                )

            elif provider == 'google':
                llm = ChatGoogleGenerativeAI(
                    model=model,
                    temperature=agent_config.temperature,
                    max_tokens=agent_config.max_tokens,
                    top_p=agent_config.top_p,
                    timeout=agent_config.timeout
                )

            logger.info(f"创建LLM实例: {provider}/{model}")
            return llm

        except Exception as e:
            logger.error(f"创建LLM实例失败: {str(e)}")
            raise

    def _get_llm_key(self, agent_type: str, agent_config) -> str:
        """生成LLM缓存键"""
        return f"{agent_type}:{agent_config.provider}:{agent_config.model}"

    def _check_circuit_breaker(self, agent_type: str) -> bool:
        """检查熔断器状态"""
        agent_config = self._get_agent_llm_config(agent_type)
        llm_key = self._get_llm_key(agent_type, agent_config)

        circuit_breaker = self.circuit_breakers.get(llm_key)
        if circuit_breaker:
            return circuit_breaker.can_proceed()
        return True

    def record_llm_performance(self, agent_type: str, success: bool, response_time: float, tokens: int = 0):
        """记录LLM性能指标"""
        agent_config = self._get_agent_llm_config(agent_type)
        llm_key = self._get_llm_key(agent_type, agent_config)

        with self._lock:
            metrics = self.performance_metrics.get(llm_key)
            if metrics:
                if success:
                    # 估算成本
                    cost = self._estimate_cost(agent_config.model, tokens)
                    metrics.update_success(response_time, tokens, cost)
                else:
                    metrics.update_failure()
                    # 记录熔断器失败
                    circuit_breaker = self.circuit_breakers.get(llm_key)
                    if circuit_breaker:
                        circuit_breaker.record_failure()

    def _estimate_cost(self, model: str, tokens: int) -> float:
        """估算LLM使用成本"""
        if model in self.cost_per_1k_tokens and tokens > 0:
            return (tokens / 1000) * self.cost_per_1k_tokens[model]
        return 0.0

    def get_performance_report(self) -> Dict[str, Any]:
        """获取性能报告"""
        report = {
            'total_agents': len(set(key.split(':')[0] for key in self.performance_metrics.keys())),
            'total_llm_instances': len(self.llm_instances),
            'performance_by_agent': {},
            'performance_by_llm': {},
            'cost_summary': {
                'total_cost': 0.0,
                'total_tokens': 0
            }
        }

        # 按智能体统计性能
        agent_metrics = defaultdict(list)
        for llm_key, metrics in self.performance_metrics.items():
            agent_type = llm_key.split(':')[0]
            agent_metrics[agent_type].append(metrics)

        for agent_type, metrics_list in agent_metrics.items():
            if metrics_list:
                total_metrics = LLMPerformanceMetrics()
                for metrics in metrics_list:
                    total_metrics.total_requests += metrics.total_requests
                    total_metrics.successful_requests += metrics.successful_requests
                    total_metrics.failed_requests += metrics.failed_requests
                    total_metrics.total_response_time += metrics.total_response_time
                    total_metrics.total_tokens += metrics.total_tokens
                    total_metrics.total_cost += metrics.total_cost

                if total_metrics.total_requests > 0:
                    total_metrics.average_response_time = total_metrics.total_response_time / total_metrics.total_requests

                report['performance_by_agent'][agent_type] = {
                    'total_requests': total_metrics.total_requests,
                    'success_rate': total_metrics.get_success_rate(),
                    'avg_response_time': total_metrics.average_response_time,
                    'total_cost': total_metrics.total_cost,
                    'total_tokens': total_metrics.total_tokens
                }

        # 按LLM统计性能
        llm_metrics = defaultdict(list)
        for llm_key, metrics in self.performance_metrics.items():
            llm_type = ':'.join(llm_key.split(':')[1:])
            llm_metrics[llm_type].append(metrics)

        for llm_type, metrics_list in llm_metrics.items():
            if metrics_list:
                total_metrics = LLMPerformanceMetrics()
                for metrics in metrics_list:
                    total_metrics.total_requests += metrics.total_requests
                    total_metrics.successful_requests += metrics.successful_requests
                    total_metrics.total_cost += metrics.total_cost

                if total_metrics.total_requests > 0:
                    report['performance_by_llm'][llm_type] = {
                        'total_requests': total_metrics.total_requests,
                        'success_rate': total_metrics.get_success_rate(),
                        'total_cost': total_metrics.total_cost
                    }

        # 总成本统计
        report['cost_summary']['total_cost'] = sum(
            metrics.total_cost for metrics in self.performance_metrics.values()
        )
        report['cost_summary']['total_tokens'] = sum(
            metrics.total_tokens for metrics in self.performance_metrics.values()
        )

        return report

    def get_agent_llm_mapping(self) -> Dict[str, Dict[str, Any]]:
        """获取智能体LLM映射"""
        mapping = {}

        agent_types = [
            'market_analyst', 'fundamentals_analyst', 'news_analyst', 'social_media_analyst',
            'bull_researcher', 'bear_researcher', 'research_manager', 'trader',
            'risky_analyst', 'safe_analyst', 'neutral_analyst', 'risk_judge'
        ]

        for agent_type in agent_types:
            config = self._get_agent_llm_config(agent_type)
            mapping[agent_type] = {
                'provider': config.provider,
                'model': config.model,
                'temperature': config.temperature,
                'max_tokens': config.max_tokens,
                'enabled': config.enabled
            }

        return mapping

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        health_report = {
            'overall_health': 'healthy',
            'healthy_agents': [],
            'unhealthy_agents': [],
            'circuit_breaker_trips': []
        }

        for llm_key, metrics in self.performance_metrics.items():
            agent_type = llm_key.split(':')[0]
            health_score = metrics.get_health_score()

            if health_score >= 0.8:
                health_report['healthy_agents'].append(agent_type)
            else:
                health_report['unhealthy_agents'].append({
                    'agent': agent_type,
                    'health_score': health_score,
                    'success_rate': metrics.get_success_rate(),
                    'consecutive_failures': metrics.consecutive_failures
                })

        # 检查熔断器状态
        for llm_key, circuit_breaker in self.circuit_breakers.items():
            if not circuit_breaker.can_proceed():
                agent_type = llm_key.split(':')[0]
                health_report['circuit_breaker_trips'].append({
                    'agent': agent_type,
                    'failure_count': circuit_breaker.get_failure_count()
                })

        # 判断整体健康状态
        if health_report['unhealthy_agents'] or health_report['circuit_breaker_trips']:
            health_report['overall_health'] = 'degraded'
        if len(health_report['unhealthy_agents']) > len(health_report['healthy_agents']):
            health_report['overall_health'] = 'unhealthy'

        return health_report

    def reload_config(self):
        """重新加载配置"""
        with self._lock:
            self.config = get_config()
            logger.info("LLM工厂配置已重新加载")

    def clear_cache(self):
        """清理LLM缓存"""
        with self._lock:
            self.llm_instances.clear()
            self.performance_metrics.clear()
            logger.info("LLM缓存已清理")

    def get_llm_cost_summary(self) -> Dict[str, float]:
        """获取LLM成本汇总"""
        total_cost = 0.0
        cost_by_provider = defaultdict(float)
        cost_by_agent = defaultdict(float)

        for llm_key, metrics in self.performance_metrics.items():
            total_cost += metrics.total_cost

            # 按供应商统计
            parts = llm_key.split(':')
            if len(parts) >= 2:
                provider = parts[1]
                cost_by_provider[provider] += metrics.total_cost

            # 按智能体统计
            agent_type = parts[0]
            cost_by_agent[agent_type] += metrics.total_cost

        return {
            'total_cost': total_cost,
            'cost_by_provider': dict(cost_by_provider),
            'cost_by_agent': dict(cost_by_agent)
        }


# 全局LLM工厂实例
llm_factory = LLMFactory()


# 便捷函数
def get_llm_for_agent(agent_type: str) -> Any:
    """获取指定智能体的LLM实例"""
    return llm_factory.get_llm_for_agent(agent_type)


def record_llm_usage(agent_type: str, success: bool, response_time: float, tokens: int = 0):
    """记录LLM使用情况"""
    llm_factory.record_llm_performance(agent_type, success, response_time, tokens)


def get_llm_performance_report() -> Dict[str, Any]:
    """获取LLM性能报告"""
    return llm_factory.get_performance_report()


def get_llm_health_report() -> Dict[str, Any]:
    """获取LLM健康报告"""
    return llm_factory.health_check()


def get_agent_llm_mapping() -> Dict[str, Dict[str, Any]]:
    """获取智能体LLM映射"""
    return llm_factory.get_agent_llm_mapping()