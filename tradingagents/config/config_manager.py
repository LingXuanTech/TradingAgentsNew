"""
统一配置管理系统
集中管理所有模块的配置信息
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradingConfig:
    """自动化交易配置"""
    watchlist: list = field(default_factory=lambda: ['AAPL', 'GOOGL', 'MSFT'])
    initial_cash: float = 100000.0
    analysis_interval: int = 30  # 分钟
    risk_check_interval: int = 5  # 分钟
    enable_auto_trading: bool = True
    enable_risk_management: bool = True
    enable_monitoring: bool = True


@dataclass
class BrokerConfig:
    """经纪商配置"""
    huatai: Dict[str, Any] = field(default_factory=lambda: {
        'enabled': False,
        'app_key': '',
        'app_secret': '',
        'account_id': '',
        'password': '',
        'sandbox': True
    })

    guangfa: Dict[str, Any] = field(default_factory=lambda: {
        'enabled': False,
        'app_key': '',
        'app_secret': '',
        'account_id': '',
        'password': ''
    })

    default_broker: str = 'huatai'


@dataclass
class TechnicalAnalysisConfig:
    """技术分析配置"""
    lookback_period: int = 100
    enable_advanced_indicators: bool = True
    enable_pattern_recognition: bool = True
    signal_threshold: float = 0.6

    # 技术指标配置
    trend_indicators: Dict[str, Any] = field(default_factory=lambda: {
        'sma_periods': [5, 10, 20, 30, 60],
        'ema_periods': [5, 10, 20, 30, 60],
        'macd': {'fast': 12, 'slow': 26, 'signal': 9},
        'adx_period': 14,
        'ichimoku': True
    })

    momentum_indicators: Dict[str, Any] = field(default_factory=lambda: {
        'rsi_period': 14,
        'stoch_k': 14,
        'stoch_d': 3,
        'williams_r': 14,
        'cci_period': 20,
        'mfi_period': 14
    })

    volatility_indicators: Dict[str, Any] = field(default_factory=lambda: {
        'bb_period': 20,
        'bb_std': 2,
        'atr_period': 14,
        'natr_period': 14
    })

    volume_indicators: Dict[str, Any] = field(default_factory=lambda: {
        'volume_sma': 20,
        'volume_roc': 12,
        'obv': True,
        'vwap': True
    })


@dataclass
class WebInterfaceConfig:
    """Web界面配置"""
    host: str = 'localhost'
    port: int = 5000
    debug: bool = False
    enable_cors: bool = True
    cors_origins: list = field(default_factory=lambda: ["*"])

    # WebSocket配置
    websocket_ping_interval: int = 25
    websocket_ping_timeout: int = 60

    # 静态文件配置
    static_folder: str = 'static'
    template_folder: str = 'templates'

    # 实时更新间隔（毫秒）
    update_intervals: Dict[str, int] = field(default_factory=lambda: {
        'market_data': 5000,      # 市场数据更新间隔
        'portfolio': 10000,       # 投资组合更新间隔
        'orders': 2000,          # 订单更新间隔
        'alerts': 3000           # 预警更新间隔
    })


@dataclass
class EmailNotificationConfig:
    """邮件通知配置"""
    enabled: bool = True
    smtp_server: str = 'smtp.qq.com'
    smtp_port: int = 587
    email_user: str = ''
    email_password: str = ''
    use_tls: bool = True
    sender_name: str = 'TradingAgents'

    # 通知选项
    notifications: Dict[str, bool] = field(default_factory=lambda: {
        'trade_alerts': True,
        'risk_alerts': True,
        'daily_reports': True,
        'system_notifications': True,
        'error_notifications': True
    })

    # 收件人列表
    recipients: list = field(default_factory=list)


@dataclass
class RiskManagementConfig:
    """风险管理配置"""
    max_position_per_stock: float = 20000.0
    max_portfolio_risk: float = 0.25
    max_daily_loss: float = 0.03
    stop_loss_ratio: float = 0.08
    take_profit_ratio: float = 0.25
    max_orders_per_day: int = 20
    min_order_interval: int = 60

    # 高级风控选项
    enable_dynamic_stop_loss: bool = True
    enable_trailing_stop: bool = False
    trailing_stop_ratio: float = 0.05


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = 'INFO'
    file_path: str = 'logs/tradingagents.log'
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = True


@dataclass
class DatabaseConfig:
    """数据库配置"""
    enabled: bool = False
    type: str = 'sqlite'  # sqlite, postgresql, mysql
    url: str = 'sqlite:///tradingagents.db'

    # PostgreSQL配置
    postgresql: Dict[str, Any] = field(default_factory=lambda: {
        'host': 'localhost',
        'port': 5432,
        'database': 'tradingagents',
        'user': 'postgres',
        'password': ''
    })


@dataclass
class AgentLLMConfig:
    """智能体LLM配置"""
    # 基础LLM配置
    provider: str = "openai"  # openai, anthropic, google, ollama, openrouter
    model: str = "gpt-4o-mini"
    backend_url: str = "https://api.openai.com/v1"

    # 模型参数
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    # 性能和成本控制
    max_requests_per_minute: int = 60
    timeout: int = 30  # 秒
    max_retries: int = 3

    # 启用状态
    enabled: bool = True


@dataclass
class SystemConfig:
    """完整系统配置"""
    # 基本信息
    version: str = '2.0.0'
    environment: str = 'development'  # development, testing, production

    # 核心配置
    trading: TradingConfig = field(default_factory=TradingConfig)
    broker: BrokerConfig = field(default_factory=BrokerConfig)
    technical_analysis: TechnicalAnalysisConfig = field(default_factory=TechnicalAnalysisConfig)
    web_interface: WebInterfaceConfig = field(default_factory=WebInterfaceConfig)
    email_notification: EmailNotificationConfig = field(default_factory=EmailNotificationConfig)
    risk_management: RiskManagementConfig = field(default_factory=RiskManagementConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)

    # LLM配置
    llm: Dict[str, AgentLLMConfig] = field(default_factory=lambda: {
        # 全局默认配置
        'default': AgentLLMConfig(),

        # 智能体特定配置
        'analysts': AgentLLMConfig(
            model="gpt-4o",
            temperature=0.3,
            max_tokens=2048
        ),
        'researchers': AgentLLMConfig(
            model="o1-preview",
            temperature=0.8,
            max_tokens=4096
        ),
        'trader': AgentLLMConfig(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=2048
        ),
        'risk_manager': AgentLLMConfig(
            model="gpt-4o",
            temperature=0.1,
            max_tokens=2048
        ),

        # 具体分析师配置
        'market_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.4,
            max_tokens=2048
        ),
        'fundamentals_analyst': AgentLLMConfig(
            model="gpt-4o",
            temperature=0.3,
            max_tokens=2048
        ),
        'news_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.4,
            max_tokens=2048
        ),
        'social_media_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.4,
            max_tokens=2048
        ),

        # 研究员配置
        'bull_researcher': AgentLLMConfig(
            model="o1-preview",
            temperature=0.7,
            max_tokens=4096
        ),
        'bear_researcher': AgentLLMConfig(
            model="o1-preview",
            temperature=0.7,
            max_tokens=4096
        ),

        # 经理配置
        'research_manager': AgentLLMConfig(
            model="o1-preview",
            temperature=0.5,
            max_tokens=4096
        ),
        'risk_judge': AgentLLMConfig(
            model="gpt-4o",
            temperature=0.1,
            max_tokens=2048
        ),

        # 风险分析师配置
        'risky_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.6,
            max_tokens=2048
        ),
        'safe_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=2048
        ),
        'neutral_analyst': AgentLLMConfig(
            model="gpt-4o-mini",
            temperature=0.4,
            max_tokens=2048
        )
    })

    # 项目路径
    project_dir: str = field(default_factory=lambda: os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir: str = field(default_factory=lambda: os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))
    logs_dir: str = field(default_factory=lambda: os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs'))


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str = None):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.default_config_file = self.project_root / 'config' / 'default_config.yaml'
        self.user_config_file = self.project_root / 'config' / 'user_config.yaml'

        # 如果没有指定配置文件，则尝试加载用户配置
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = self.user_config_file if self.user_config_file.exists() else self.default_config_file

        # 当前配置
        self.config: Optional[SystemConfig] = None

        # 加载配置
        self.load_config()

    def load_config(self) -> SystemConfig:
        """加载配置文件"""
        try:
            # 确保配置目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # 如果配置文件不存在，创建默认配置
            if not self.config_file.exists():
                self._create_default_config()

            # 加载配置
            if self.config_file.suffix.lower() in ['.yaml', '.yml']:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            elif self.config_file.suffix.lower() == '.json':
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {self.config_file.suffix}")

            # 解析配置
            self.config = self._parse_config(config_data)

            logger.info(f"配置加载成功: {self.config_file}")
            return self.config

        except Exception as e:
            logger.error(f"配置加载失败: {str(e)}")
            # 返回默认配置
            return self._create_default_config()

    def _create_default_config(self) -> SystemConfig:
        """创建默认配置"""
        try:
            # 创建默认配置对象
            self.config = SystemConfig()

            # 保存到文件
            self.save_config()

            logger.info(f"已创建默认配置: {self.config_file}")
            return self.config

        except Exception as e:
            logger.error(f"创建默认配置失败: {str(e)}")
            # 返回内存中的默认配置
            return SystemConfig()

    def _parse_config(self, config_data: Dict[str, Any]) -> SystemConfig:
        """解析配置数据"""
        try:
            # 创建系统配置对象
            system_config = SystemConfig()

            # 更新基本信息
            if 'version' in config_data:
                system_config.version = config_data['version']
            if 'environment' in config_data:
                system_config.environment = config_data['environment']

            # 解析各模块配置
            if 'trading' in config_data:
                system_config.trading = self._parse_trading_config(config_data['trading'])

            if 'broker' in config_data:
                system_config.broker = self._parse_broker_config(config_data['broker'])

            if 'technical_analysis' in config_data:
                system_config.technical_analysis = self._parse_technical_analysis_config(config_data['technical_analysis'])

            if 'web_interface' in config_data:
                system_config.web_interface = self._parse_web_interface_config(config_data['web_interface'])

            if 'email_notification' in config_data:
                system_config.email_notification = self._parse_email_notification_config(config_data['email_notification'])

            if 'risk_management' in config_data:
                system_config.risk_management = self._parse_risk_management_config(config_data['risk_management'])

            if 'logging' in config_data:
                system_config.logging = self._parse_logging_config(config_data['logging'])

            if 'database' in config_data:
                system_config.database = self._parse_database_config(config_data['database'])

            if 'llm' in config_data:
                system_config.llm = self._parse_llm_config(config_data['llm'])

            return system_config

        except Exception as e:
            logger.error(f"配置解析失败: {str(e)}")
            return SystemConfig()

    def _parse_trading_config(self, config_data: Dict[str, Any]) -> TradingConfig:
        """解析交易配置"""
        trading_config = TradingConfig()

        if 'watchlist' in config_data:
            trading_config.watchlist = config_data['watchlist']
        if 'initial_cash' in config_data:
            trading_config.initial_cash = config_data['initial_cash']
        if 'analysis_interval' in config_data:
            trading_config.analysis_interval = config_data['analysis_interval']
        if 'risk_check_interval' in config_data:
            trading_config.risk_check_interval = config_data['risk_check_interval']
        if 'enable_auto_trading' in config_data:
            trading_config.enable_auto_trading = config_data['enable_auto_trading']
        if 'enable_risk_management' in config_data:
            trading_config.enable_risk_management = config_data['enable_risk_management']
        if 'enable_monitoring' in config_data:
            trading_config.enable_monitoring = config_data['enable_monitoring']

        return trading_config

    def _parse_broker_config(self, config_data: Dict[str, Any]) -> BrokerConfig:
        """解析经纪商配置"""
        broker_config = BrokerConfig()

        if 'huatai' in config_data:
            broker_config.huatai.update(config_data['huatai'])
        if 'guangfa' in config_data:
            broker_config.guangfa.update(config_data['guangfa'])
        if 'default_broker' in config_data:
            broker_config.default_broker = config_data['default_broker']

        return broker_config

    def _parse_technical_analysis_config(self, config_data: Dict[str, Any]) -> TechnicalAnalysisConfig:
        """解析技术分析配置"""
        ta_config = TechnicalAnalysisConfig()

        if 'lookback_period' in config_data:
            ta_config.lookback_period = config_data['lookback_period']
        if 'enable_advanced_indicators' in config_data:
            ta_config.enable_advanced_indicators = config_data['enable_advanced_indicators']
        if 'enable_pattern_recognition' in config_data:
            ta_config.enable_pattern_recognition = config_data['enable_pattern_recognition']
        if 'signal_threshold' in config_data:
            ta_config.signal_threshold = config_data['signal_threshold']

        # 解析嵌套配置
        for section in ['trend_indicators', 'momentum_indicators', 'volatility_indicators', 'volume_indicators']:
            if section in config_data:
                getattr(ta_config, section).update(config_data[section])

        return ta_config

    def _parse_web_interface_config(self, config_data: Dict[str, Any]) -> WebInterfaceConfig:
        """解析Web界面配置"""
        web_config = WebInterfaceConfig()

        if 'host' in config_data:
            web_config.host = config_data['host']
        if 'port' in config_data:
            web_config.port = config_data['port']
        if 'debug' in config_data:
            web_config.debug = config_data['debug']
        if 'enable_cors' in config_data:
            web_config.enable_cors = config_data['enable_cors']
        if 'cors_origins' in config_data:
            web_config.cors_origins = config_data['cors_origins']
        if 'update_intervals' in config_data:
            web_config.update_intervals.update(config_data['update_intervals'])

        return web_config

    def _parse_email_notification_config(self, config_data: Dict[str, Any]) -> EmailNotificationConfig:
        """解析邮件通知配置"""
        email_config = EmailNotificationConfig()

        if 'enabled' in config_data:
            email_config.enabled = config_data['enabled']
        if 'smtp_server' in config_data:
            email_config.smtp_server = config_data['smtp_server']
        if 'smtp_port' in config_data:
            email_config.smtp_port = config_data['smtp_port']
        if 'email_user' in config_data:
            email_config.email_user = config_data['email_user']
        if 'email_password' in config_data:
            email_config.email_password = config_data['email_password']
        if 'use_tls' in config_data:
            email_config.use_tls = config_data['use_tls']
        if 'sender_name' in config_data:
            email_config.sender_name = config_data['sender_name']
        if 'notifications' in config_data:
            email_config.notifications.update(config_data['notifications'])
        if 'recipients' in config_data:
            email_config.recipients = config_data['recipients']

        return email_config

    def _parse_risk_management_config(self, config_data: Dict[str, Any]) -> RiskManagementConfig:
        """解析风险管理配置"""
        risk_config = RiskManagementConfig()

        for field in ['max_position_per_stock', 'max_portfolio_risk', 'max_daily_loss',
                     'stop_loss_ratio', 'take_profit_ratio', 'max_orders_per_day',
                     'min_order_interval', 'enable_dynamic_stop_loss', 'enable_trailing_stop',
                     'trailing_stop_ratio']:
            if field in config_data:
                setattr(risk_config, field, config_data[field])

        return risk_config

    def _parse_logging_config(self, config_data: Dict[str, Any]) -> LoggingConfig:
        """解析日志配置"""
        logging_config = LoggingConfig()

        if 'level' in config_data:
            logging_config.level = config_data['level']
        if 'file_path' in config_data:
            logging_config.file_path = config_data['file_path']
        if 'max_file_size' in config_data:
            logging_config.max_file_size = config_data['max_file_size']
        if 'backup_count' in config_data:
            logging_config.backup_count = config_data['backup_count']
        if 'enable_console' in config_data:
            logging_config.enable_console = config_data['enable_console']
        if 'enable_file' in config_data:
            logging_config.enable_file = config_data['enable_file']

        return logging_config

    def _parse_database_config(self, config_data: Dict[str, Any]) -> DatabaseConfig:
        """解析数据库配置"""
        db_config = DatabaseConfig()

        if 'enabled' in config_data:
            db_config.enabled = config_data['enabled']
        if 'type' in config_data:
            db_config.type = config_data['type']
        if 'url' in config_data:
            db_config.url = config_data['url']
        if 'postgresql' in config_data:
            db_config.postgresql.update(config_data['postgresql'])

        return db_config

    def _parse_llm_config(self, config_data: Dict[str, Any]) -> Dict[str, AgentLLMConfig]:
        """解析LLM配置"""
        llm_configs = {}

        for agent_name, agent_config in config_data.items():
            if isinstance(agent_config, dict):
                llm_config = AgentLLMConfig()

                # 解析基本配置
                for field in ['provider', 'model', 'backend_url', 'temperature', 'max_tokens',
                             'top_p', 'frequency_penalty', 'presence_penalty', 'max_requests_per_minute',
                             'timeout', 'max_retries', 'enabled']:
                    if field in agent_config:
                        setattr(llm_config, field, agent_config[field])

                llm_configs[agent_name] = llm_config
            else:
                # 如果不是字典，保持原有的AgentLLMConfig
                llm_configs[agent_name] = agent_config

        return llm_configs

    def save_config(self, config_file: str = None) -> bool:
        """保存配置到文件"""
        try:
            file_path = Path(config_file) if config_file else self.config_file

            # 确保目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 转换配置对象为字典
            config_dict = self._config_to_dict()

            # 保存为YAML格式
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的配置文件格式: {file_path.suffix}")

            logger.info(f"配置保存成功: {file_path}")
            return True

        except Exception as e:
            logger.error(f"配置保存失败: {str(e)}")
            return False

    def _config_to_dict(self) -> Dict[str, Any]:
        """将配置对象转换为字典"""
        if not self.config:
            return {}

        config_dict = {
            'version': self.config.version,
            'environment': self.config.environment,
            'trading': {
                'watchlist': self.config.trading.watchlist,
                'initial_cash': self.config.trading.initial_cash,
                'analysis_interval': self.config.trading.analysis_interval,
                'risk_check_interval': self.config.trading.risk_check_interval,
                'enable_auto_trading': self.config.trading.enable_auto_trading,
                'enable_risk_management': self.config.trading.enable_risk_management,
                'enable_monitoring': self.config.trading.enable_monitoring
            },
            'broker': {
                'huatai': self.config.broker.huatai,
                'guangfa': self.config.broker.guangfa,
                'default_broker': self.config.broker.default_broker
            },
            'technical_analysis': {
                'lookback_period': self.config.technical_analysis.lookback_period,
                'enable_advanced_indicators': self.config.technical_analysis.enable_advanced_indicators,
                'enable_pattern_recognition': self.config.technical_analysis.enable_pattern_recognition,
                'signal_threshold': self.config.technical_analysis.signal_threshold,
                'trend_indicators': self.config.technical_analysis.trend_indicators,
                'momentum_indicators': self.config.technical_analysis.momentum_indicators,
                'volatility_indicators': self.config.technical_analysis.volatility_indicators,
                'volume_indicators': self.config.technical_analysis.volume_indicators
            },
            'web_interface': {
                'host': self.config.web_interface.host,
                'port': self.config.web_interface.port,
                'debug': self.config.web_interface.debug,
                'enable_cors': self.config.web_interface.enable_cors,
                'cors_origins': self.config.web_interface.cors_origins,
                'update_intervals': self.config.web_interface.update_intervals
            },
            'email_notification': {
                'enabled': self.config.email_notification.enabled,
                'smtp_server': self.config.email_notification.smtp_server,
                'smtp_port': self.config.email_notification.smtp_port,
                'email_user': self.config.email_notification.email_user,
                'email_password': self.config.email_notification.email_password,
                'use_tls': self.config.email_notification.use_tls,
                'sender_name': self.config.email_notification.sender_name,
                'notifications': self.config.email_notification.notifications,
                'recipients': self.config.email_notification.recipients
            },
            'risk_management': {
                'max_position_per_stock': self.config.risk_management.max_position_per_stock,
                'max_portfolio_risk': self.config.risk_management.max_portfolio_risk,
                'max_daily_loss': self.config.risk_management.max_daily_loss,
                'stop_loss_ratio': self.config.risk_management.stop_loss_ratio,
                'take_profit_ratio': self.config.risk_management.take_profit_ratio,
                'max_orders_per_day': self.config.risk_management.max_orders_per_day,
                'min_order_interval': self.config.risk_management.min_order_interval,
                'enable_dynamic_stop_loss': self.config.risk_management.enable_dynamic_stop_loss,
                'enable_trailing_stop': self.config.risk_management.enable_trailing_stop,
                'trailing_stop_ratio': self.config.risk_management.trailing_stop_ratio
            },
            'logging': {
                'level': self.config.logging.level,
                'file_path': self.config.logging.file_path,
                'max_file_size': self.config.logging.max_file_size,
                'backup_count': self.config.logging.backup_count,
                'enable_console': self.config.logging.enable_console,
                'enable_file': self.config.logging.enable_file
            },
            'database': {
                'enabled': self.config.database.enabled,
                'type': self.config.database.type,
                'url': self.config.database.url,
                'postgresql': self.config.database.postgresql
            },
            'llm': self.config.llm
        }

        return config_dict

    def get_config(self) -> SystemConfig:
        """获取当前配置"""
        if not self.config:
            self.load_config()
        return self.config

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """更新配置"""
        try:
            # 解析更新后的配置
            if 'trading' in updates:
                self.config.trading = self._parse_trading_config(updates['trading'])
            if 'broker' in updates:
                self.config.broker = self._parse_broker_config(updates['broker'])
            if 'technical_analysis' in updates:
                self.config.technical_analysis = self._parse_technical_analysis_config(updates['technical_analysis'])
            if 'web_interface' in updates:
                self.config.web_interface = self._parse_web_interface_config(updates['web_interface'])
            if 'email_notification' in updates:
                self.config.email_notification = self._parse_email_notification_config(updates['email_notification'])
            if 'risk_management' in updates:
                self.config.risk_management = self._parse_risk_management_config(updates['risk_management'])

            # 保存配置
            self.save_config()

            logger.info("配置更新成功")
            return True

        except Exception as e:
            logger.error(f"配置更新失败: {str(e)}")
            return False

    def validate_config(self) -> List[str]:
        """验证配置有效性"""
        errors = []

        try:
            config = self.get_config()

            # 验证交易配置
            if config.trading.initial_cash <= 0:
                errors.append("初始资金必须大于0")
            if config.trading.analysis_interval <= 0:
                errors.append("分析间隔必须大于0")
            if not config.trading.watchlist:
                errors.append("股票池不能为空")

            # 验证经纪商配置
            if config.broker.huatai['enabled'] and not config.broker.huatai['app_key']:
                errors.append("华泰证券app_key不能为空")
            if config.broker.guangfa['enabled'] and not config.broker.guangfa['app_key']:
                errors.append("广发证券app_key不能为空")

            # 验证邮件配置
            if config.email_notification.enabled:
                if not config.email_notification.email_user:
                    errors.append("邮件用户名不能为空")
                if not config.email_notification.email_password:
                    errors.append("邮件密码不能为空")
                if not config.email_notification.recipients:
                    errors.append("邮件收件人不能为空")

            # 验证Web界面配置
            if config.web_interface.port <= 0 or config.web_interface.port > 65535:
                errors.append("Web端口号必须在1-65535之间")

        except Exception as e:
            errors.append(f"配置验证失败: {str(e)}")

        return errors


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> SystemConfig:
    """获取全局配置"""
    return config_manager.get_config()


def load_config(config_file: str = None) -> SystemConfig:
    """加载配置"""
    global config_manager
    if config_file:
        config_manager = ConfigManager(config_file)
    return config_manager.load_config()


def save_config(config_file: str = None) -> bool:
    """保存配置"""
    return config_manager.save_config(config_file)


def update_config(updates: Dict[str, Any]) -> bool:
    """更新配置"""
    return config_manager.update_config(updates)


def validate_config() -> List[str]:
    """验证配置"""
    return config_manager.validate_config()