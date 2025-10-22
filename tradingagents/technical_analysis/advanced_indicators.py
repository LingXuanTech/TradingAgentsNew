"""
高级技术指标库
扩展原有技术指标，提供更多分析方法
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import talib
import pandas_ta as ta

# 导入配置管理器
from ..config.config_manager import get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TechnicalSignal:
    """技术信号"""
    symbol: str
    signal_type: str  # 'buy', 'sell', 'hold', 'strong_buy', 'strong_sell'
    strength: float   # 信号强度 0-1
    indicators: Dict[str, float]  # 支撑指标值
    timestamp: datetime
    confidence: float = 0.8  # 置信度


@dataclass
class SupportResistance:
    """支撑阻力位"""
    symbol: str
    support_levels: List[float]
    resistance_levels: List[float]
    strength: Dict[float, float]  # 价位强度
    timestamp: datetime


class AdvancedTechnicalAnalyzer:
    """高级技术分析器"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化高级技术分析器

        Args:
            config: 技术分析配置，如果为None则从配置文件读取
        """
        # 获取系统配置
        system_config = get_config()

        # 如果没有传入配置，则使用系统配置中的技术分析配置
        if config is None:
            ta_config = system_config.technical_analysis
            self.lookback_period = ta_config.lookback_period
            self.indicator_configs = {
                'trend': ta_config.trend_indicators,
                'momentum': ta_config.momentum_indicators,
                'volatility': ta_config.volatility_indicators,
                'volume': ta_config.volume_indicators
            }
            self.signal_threshold = ta_config.signal_threshold
        else:
            # 使用传入的配置
            self.lookback_period = config.get('lookback_period', 100)
            self.indicator_configs = config.get('indicator_configs', {})
            self.signal_threshold = config.get('signal_threshold', 0.6)

    def analyze_comprehensive(self, df: pd.DataFrame, symbol: str = "UNKNOWN") -> Dict[str, Any]:
        """
        综合技术分析

        Args:
            df: 股票数据DataFrame，必须包含OHLCV列
            symbol: 股票代码

        Returns:
            综合分析结果
        """
        try:
            # 验证数据完整性
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"数据缺少必要列: {required_columns}")

            # 计算所有技术指标
            indicators = self._calculate_all_indicators(df)

            # 生成交易信号
            signals = self._generate_signals(df, indicators)

            # 识别支撑阻力位
            support_resistance = self._identify_support_resistance(df)

            # 趋势分析
            trend_analysis = self._analyze_trend(df, indicators)

            # 形态识别
            patterns = self._identify_patterns(df)

            # 综合评分
            score = self._calculate_composite_score(indicators, signals)

            return {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'indicators': indicators,
                'signals': signals,
                'support_resistance': support_resistance,
                'trend_analysis': trend_analysis,
                'patterns': patterns,
                'composite_score': score,
                'recommendation': self._generate_recommendation(score, signals)
            }

        except Exception as e:
            logger.error(f"综合技术分析失败 {symbol}: {str(e)}")
            return {}

    def _calculate_all_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """计算所有技术指标"""
        indicators = {}

        try:
            # 趋势指标
            indicators['trend'] = self._calculate_trend_indicators(df)

            # 动量指标
            indicators['momentum'] = self._calculate_momentum_indicators(df)

            # 波动率指标
            indicators['volatility'] = self._calculate_volatility_indicators(df)

            # 成交量指标
            indicators['volume'] = self._calculate_volume_indicators(df)

            # 高级指标
            indicators['advanced'] = self._calculate_advanced_indicators(df)

            return indicators

        except Exception as e:
            logger.error(f"计算技术指标失败: {str(e)}")
            return {}

    def _calculate_trend_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算趋势指标"""
        trend_data = {}

        try:
            close = df['Close'].values

            # 移动平均线
            for period in self.indicator_configs['trend']['sma_periods']:
                trend_data[f'sma_{period}'] = talib.SMA(close, timeperiod=period)[-1]

            for period in self.indicator_configs['trend']['ema_periods']:
                trend_data[f'ema_{period}'] = talib.EMA(close, timeperiod=period)[-1]

            # MACD
            macd_config = self.indicator_configs['trend']['macd']
            macd, macdsignal, macdhist = talib.MACD(
                close,
                fastperiod=macd_config['fast'],
                slowperiod=macd_config['slow'],
                signalperiod=macd_config['signal']
            )
            trend_data['macd'] = macd[-1]
            trend_data['macd_signal'] = macdsignal[-1]
            trend_data['macd_hist'] = macdhist[-1]

            # ADX (平均趋向指数)
            adx_period = self.indicator_configs['trend']['adx_period']
            trend_data['adx'] = talib.ADX(df['High'], df['Low'], close, timeperiod=adx_period)[-1]

            # DMI (趋向指标)
            plus_di = talib.PLUS_DI(df['High'], df['Low'], close, timeperiod=adx_period)[-1]
            minus_di = talib.MINUS_DI(df['High'], df['Low'], close, timeperiod=adx_period)[-1]
            trend_data['plus_di'] = plus_di
            trend_data['minus_di'] = minus_di

            return trend_data

        except Exception as e:
            logger.error(f"计算趋势指标失败: {str(e)}")
            return {}

    def _calculate_momentum_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算动量指标"""
        momentum_data = {}

        try:
            close = df['Close'].values
            high = df['High'].values
            low = df['Low'].values

            # RSI
            rsi_period = self.indicator_configs['momentum']['rsi_period']
            momentum_data['rsi'] = talib.RSI(close, timeperiod=rsi_period)[-1]

            # 随机指标
            stoch_config = self.indicator_configs['momentum']
            slowk, slowd = talib.STOCH(
                high, low, close,
                fastk_period=stoch_config['stoch_k'],
                slowk_period=stoch_config['stoch_k'],
                slowd_period=stoch_config['stoch_d']
            )
            momentum_data['stoch_k'] = slowk[-1]
            momentum_data['stoch_d'] = slowd[-1]

            # Williams %R
            momentum_data['williams_r'] = talib.WILLR(high, low, close, timeperiod=stoch_config['williams_r'])[-1]

            # CCI (顺势指标)
            momentum_data['cci'] = talib.CCI(high, low, close, timeperiod=stoch_config['cci_period'])[-1]

            # MFI (资金流量指标)
            momentum_data['mfi'] = talib.MFI(high, low, close, df['Volume'], timeperiod=stoch_config['mfi_period'])[-1]

            # ROC (变动率指标)
            momentum_data['roc'] = talib.ROC(close, timeperiod=10)[-1]

            # 威廉变异离散量
            momentum_data['williams_ad'] = talib.AD(high, low, close, df['Volume'])[-1]

            return momentum_data

        except Exception as e:
            logger.error(f"计算动量指标失败: {str(e)}")
            return {}

    def _calculate_volatility_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算波动率指标"""
        volatility_data = {}

        try:
            close = df['Close'].values
            high = df['High'].values
            low = df['Low'].values

            # 布林带
            bb_period = self.indicator_configs['volatility']['bb_period']
            bb_std = self.indicator_configs['volatility']['bb_std']

            upperband, middleband, lowerband = talib.BBANDS(
                close,
                timeperiod=bb_period,
                nbdevup=bb_std,
                nbdevdn=bb_std,
                matype=0
            )

            volatility_data['bb_upper'] = upperband[-1]
            volatility_data['bb_middle'] = middleband[-1]
            volatility_data['bb_lower'] = lowerband[-1]
            volatility_data['bb_width'] = (upperband[-1] - lowerband[-1]) / middleband[-1]

            # ATR (平均真实范围)
            atr_period = self.indicator_configs['volatility']['atr_period']
            volatility_data['atr'] = talib.ATR(high, low, close, timeperiod=atr_period)[-1]

            # NATR (归一化平均真实范围)
            volatility_data['natr'] = talib.NATR(high, low, close, timeperiod=atr_period)[-1]

            return volatility_data

        except Exception as e:
            logger.error(f"计算波动率指标失败: {str(e)}")
            return {}

    def _calculate_volume_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算成交量指标"""
        volume_data = {}

        try:
            close = df['Close'].values
            volume = df['Volume'].values

            # 成交量移动平均
            volume_sma_period = self.indicator_configs['volume']['volume_sma']
            volume_data['volume_sma'] = talib.SMA(volume, timeperiod=volume_sma_period)[-1]

            # 成交量变化率
            volume_roc_period = self.indicator_configs['volume']['volume_roc']
            volume_data['volume_roc'] = talib.ROC(volume, timeperiod=volume_roc_period)[-1]

            # OBV (能量潮指标)
            volume_data['obv'] = talib.OBV(close, volume)[-1]

            # AD (累积/分布线)
            volume_data['ad'] = talib.AD(df['High'], df['Low'], close, volume)[-1]

            #ADOSC (A/D振荡器)
            volume_data['adosc'] = talib.ADOSC(high=df['High'], low=df['Low'], close=close, volume=volume, fastperiod=3, slowperiod=10)[-1]

            return volume_data

        except Exception as e:
            logger.error(f"计算成交量指标失败: {str(e)}")
            return {}

    def _calculate_advanced_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算高级指标"""
        advanced_data = {}

        try:
            close = df['Close'].values
            high = df['High'].values
            low = df['Low'].values
            volume = df['Volume'].values

            # 希金阿诗烛线模式识别
            advanced_data['cdl_hammer'] = talib.CDLHAMMER(high, low, close)[-1]
            advanced_data['cdl_shooting_star'] = talib.CDLSHOOTINGSTAR(high, low, close)[-1]
            advanced_data['cdl_morning_star'] = talib.CDLMORNINGSTAR(high, low, close)[-1]
            advanced_data['cdl_evening_star'] = talib.CDLEVENINGSTAR(high, low, close)[-1]

            # 动量指标
            advanced_data['apo'] = talib.APO(close, fastperiod=12, slowperiod=26)[-1]  # 绝对价格振荡器
            advanced_data['ppo'] = talib.PPO(close, fastperiod=12, slowperiod=26)[-1]  # 百分比价格振荡器

            # 随机动量指标
            advanced_data['stochrsi_fastk'], advanced_data['stochrsi_fastd'] = talib.STOCHRSI(
                close, timeperiod=14, fastk_period=3, fastd_period=3
            )[-1:]

            return advanced_data

        except Exception as e:
            logger.error(f"计算高级指标失败: {str(e)}")
            return {}

    def _generate_signals(self, df: pd.DataFrame, indicators: Dict) -> List[TechnicalSignal]:
        """生成技术信号"""
        signals = []

        try:
            current_price = df['Close'].iloc[-1]

            # 趋势信号
            trend_signal = self._trend_signal(indicators, current_price)
            if trend_signal:
                signals.append(trend_signal)

            # 动量信号
            momentum_signal = self._momentum_signal(indicators, current_price)
            if momentum_signal:
                signals.append(momentum_signal)

            # 波动率信号
            volatility_signal = self._volatility_signal(indicators, current_price)
            if volatility_signal:
                signals.append(volatility_signal)

            # 成交量信号
            volume_signal = self._volume_signal(indicators, current_price)
            if volume_signal:
                signals.append(volume_signal)

            return signals

        except Exception as e:
            logger.error(f"生成技术信号失败: {str(e)}")
            return []

    def _trend_signal(self, indicators: Dict, price: float) -> Optional[TechnicalSignal]:
        """趋势信号"""
        try:
            trend_indicators = indicators.get('trend', {})

            # 均线排列信号
            sma_5 = trend_indicators.get('sma_5', 0)
            sma_10 = trend_indicators.get('sma_10', 0)
            sma_20 = trend_indicators.get('sma_20', 0)

            if sma_5 > sma_10 > sma_20 and price > sma_5:
                return TechnicalSignal(
                    symbol="TREND",
                    signal_type="buy",
                    strength=0.8,
                    indicators={'sma_alignment': 0.8},
                    timestamp=datetime.now()
                )

            if sma_5 < sma_10 < sma_20 and price < sma_5:
                return TechnicalSignal(
                    symbol="TREND",
                    signal_type="sell",
                    strength=0.8,
                    indicators={'sma_alignment': -0.8},
                    timestamp=datetime.now()
                )

            # MACD信号
            macd = trend_indicators.get('macd', 0)
            macd_signal = trend_indicators.get('macd_signal', 0)

            if macd > macd_signal and price > sma_10:
                return TechnicalSignal(
                    symbol="MACD",
                    signal_type="buy",
                    strength=0.7,
                    indicators={'macd_diff': macd - macd_signal},
                    timestamp=datetime.now()
                )

            return None

        except Exception as e:
            logger.error(f"趋势信号生成失败: {str(e)}")
            return None

    def _momentum_signal(self, indicators: Dict, price: float) -> Optional[TechnicalSignal]:
        """动量信号"""
        try:
            momentum_indicators = indicators.get('momentum', {})

            # RSI信号
            rsi = momentum_indicators.get('rsi', 50)

            if rsi < 30:
                return TechnicalSignal(
                    symbol="RSI",
                    signal_type="buy",
                    strength=0.9,
                    indicators={'rsi': rsi},
                    timestamp=datetime.now()
                )
            elif rsi > 70:
                return TechnicalSignal(
                    symbol="RSI",
                    signal_type="sell",
                    strength=0.9,
                    indicators={'rsi': rsi},
                    timestamp=datetime.now()
                )

            # 随机指标信号
            stoch_k = momentum_indicators.get('stoch_k', 50)
            stoch_d = momentum_indicators.get('stoch_d', 50)

            if stoch_k < 20 and stoch_k > stoch_d:
                return TechnicalSignal(
                    symbol="STOCH",
                    signal_type="buy",
                    strength=0.7,
                    indicators={'stoch_k': stoch_k, 'stoch_d': stoch_d},
                    timestamp=datetime.now()
                )
            elif stoch_k > 80 and stoch_k < stoch_d:
                return TechnicalSignal(
                    symbol="STOCH",
                    signal_type="sell",
                    strength=0.7,
                    indicators={'stoch_k': stoch_k, 'stoch_d': stoch_d},
                    timestamp=datetime.now()
                )

            return None

        except Exception as e:
            logger.error(f"动量信号生成失败: {str(e)}")
            return None

    def _volatility_signal(self, indicators: Dict, price: float) -> Optional[TechnicalSignal]:
        """波动率信号"""
        try:
            volatility_indicators = indicators.get('volatility', {})

            # 布林带信号
            bb_upper = volatility_indicators.get('bb_upper', 0)
            bb_lower = volatility_indicators.get('bb_lower', 0)
            bb_middle = volatility_indicators.get('bb_middle', 0)

            if price <= bb_lower:
                return TechnicalSignal(
                    symbol="BB",
                    signal_type="buy",
                    strength=0.8,
                    indicators={'bb_position': (price - bb_middle) / (bb_upper - bb_middle)},
                    timestamp=datetime.now()
                )
            elif price >= bb_upper:
                return TechnicalSignal(
                    symbol="BB",
                    signal_type="sell",
                    strength=0.8,
                    indicators={'bb_position': (price - bb_middle) / (bb_upper - bb_middle)},
                    timestamp=datetime.now()
                )

            return None

        except Exception as e:
            logger.error(f"波动率信号生成失败: {str(e)}")
            return None

    def _volume_signal(self, indicators: Dict, price: float) -> Optional[TechnicalSignal]:
        """成交量信号"""
        try:
            volume_indicators = indicators.get('volume', {})

            # OBV趋势信号
            obv = volume_indicators.get('obv', 0)
            volume_sma = volume_indicators.get('volume_sma', 1)

            if obv > 0 and price > volume_sma:
                return TechnicalSignal(
                    symbol="OBV",
                    signal_type="buy",
                    strength=0.6,
                    indicators={'obv_trend': obv},
                    timestamp=datetime.now()
                )

            return None

        except Exception as e:
            logger.error(f"成交量信号生成失败: {str(e)}")
            return None

    def _identify_support_resistance(self, df: pd.DataFrame) -> SupportResistance:
        """识别支撑阻力位"""
        try:
            # 简化版支撑阻力识别
            recent_highs = df['High'].tail(20).tolist()
            recent_lows = df['Low'].tail(20).tolist()

            # 找出关键价位（简化算法）
            support_levels = sorted(list(set([round(x, 2) for x in recent_lows if x > df['Close'].iloc[-1] * 0.95])))
            resistance_levels = sorted(list(set([round(x, 2) for x in recent_highs if x < df['Close'].iloc[-1] * 1.05])))

            # 计算强度（简化）
            strength = {}
            for level in support_levels + resistance_levels:
                strength[level] = 0.7

            return SupportResistance(
                symbol="UNKNOWN",
                support_levels=support_levels[:3],  # 取前3个
                resistance_levels=resistance_levels[-3:],  # 取最后3个（最高的）
                strength=strength,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"支撑阻力识别失败: {str(e)}")
            return SupportResistance("UNKNOWN", [], [], {}, datetime.now())

    def _analyze_trend(self, df: pd.DataFrame, indicators: Dict) -> Dict[str, Any]:
        """趋势分析"""
        try:
            trend_indicators = indicators.get('trend', {})

            # 简单趋势判断
            sma_5 = trend_indicators.get('sma_5', 0)
            sma_20 = trend_indicators.get('sma_20', 0)
            current_price = df['Close'].iloc[-1]

            if sma_5 > sma_20 and current_price > sma_5:
                trend = "bullish"
                strength = min(1.0, (sma_5 - sma_20) / sma_20)
            elif sma_5 < sma_20 and current_price < sma_5:
                trend = "bearish"
                strength = min(1.0, (sma_20 - sma_5) / sma_20)
            else:
                trend = "sideways"
                strength = 0.3

            return {
                'trend': trend,
                'strength': strength,
                'trend_score': 1.0 if trend == "bullish" else (-1.0 if trend == "bearish" else 0.0)
            }

        except Exception as e:
            logger.error(f"趋势分析失败: {str(e)}")
            return {'trend': 'unknown', 'strength': 0.0, 'trend_score': 0.0}

    def _identify_patterns(self, df: pd.DataFrame) -> List[str]:
        """识别技术形态"""
        patterns = []

        try:
            # 简化版形态识别
            recent_data = df.tail(10)

            # 检查是否形成锤头线
            if self._is_hammer_pattern(recent_data):
                patterns.append("hammer")

            # 检查是否形成启明星
            if self._is_morning_star_pattern(recent_data):
                patterns.append("morning_star")

            # 检查是否形成黄昏星
            if self._is_evening_star_pattern(recent_data):
                patterns.append("evening_star")

            return patterns

        except Exception as e:
            logger.error(f"形态识别失败: {str(e)}")
            return []

    def _is_hammer_pattern(self, df: pd.DataFrame) -> bool:
        """锤头线形态识别"""
        # 简化实现
        return False

    def _is_morning_star_pattern(self, df: pd.DataFrame) -> bool:
        """启明星形态识别"""
        # 简化实现
        return False

    def _is_evening_star_pattern(self, df: pd.DataFrame) -> bool:
        """黄昏星形态识别"""
        # 简化实现
        return False

    def _calculate_composite_score(self, indicators: Dict, signals: List[TechnicalSignal]) -> float:
        """计算综合评分"""
        try:
            score = 0.0

            # 趋势评分
            trend_score = indicators.get('trend_analysis', {}).get('trend_score', 0)
            score += trend_score * 0.4

            # 信号评分
            signal_scores = []
            for signal in signals:
                if signal.signal_type in ['buy', 'strong_buy']:
                    signal_scores.append(signal.strength)
                elif signal.signal_type in ['sell', 'strong_sell']:
                    signal_scores.append(-signal.strength)

            if signal_scores:
                avg_signal_score = sum(signal_scores) / len(signal_scores)
                score += avg_signal_score * 0.6

            # 限制在-1到1之间
            return max(-1.0, min(1.0, score))

        except Exception as e:
            logger.error(f"综合评分计算失败: {str(e)}")
            return 0.0

    def _generate_recommendation(self, score: float, signals: List[TechnicalSignal]) -> str:
        """生成投资建议"""
        if score > 0.6:
            return "强烈推荐买入"
        elif score > 0.2:
            return "建议买入"
        elif score > -0.2:
            return "持有观望"
        elif score > -0.6:
            return "建议卖出"
        else:
            return "强烈推荐卖出"


# 便捷函数
def quick_technical_analysis(df: pd.DataFrame, symbol: str = "UNKNOWN") -> Dict[str, Any]:
    """
    快速技术分析

    Args:
        df: 股票数据
        symbol: 股票代码

    Returns:
        分析结果
    """
    analyzer = AdvancedTechnicalAnalyzer()
    return analyzer.analyze_comprehensive(df, symbol)


def get_technical_signals(df: pd.DataFrame, symbol: str = "UNKNOWN") -> List[TechnicalSignal]:
    """
    获取技术信号

    Args:
        df: 股票数据
        symbol: 股票代码

    Returns:
        技术信号列表
    """
    analyzer = AdvancedTechnicalAnalyzer()
    result = analyzer.analyze_comprehensive(df, symbol)
    return result.get('signals', [])