"""
邮件通知服务
用于发送交易提醒、风险预警、日报表等通知
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 导入配置管理器
from ..config.config_manager import get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailConfig:
    """邮件配置"""
    smtp_server: str = "smtp.qq.com"  # QQ邮箱
    smtp_port: int = 587
    email_user: str = ""
    email_password: str = ""
    use_tls: bool = True
    sender_name: str = "TradingAgents"


class EmailTemplate:
    """邮件模板"""

    # 交易提醒模板
    TRADE_ALERT = """
    <html>
    <body>
        <h2>📈 交易提醒</h2>
        <p>亲爱的用户，</p>
        <p>系统检测到交易信号：</p>
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
            <p><strong>股票代码：</strong>{symbol}</p>
            <p><strong>交易类型：</strong>{trade_type}</p>
            <p><strong>交易数量：</strong>{quantity}</p>
            <p><strong>交易价格：</strong>¥{price}</p>
            <p><strong>信号强度：</strong>{confidence}</p>
            <p><strong>生成时间：</strong>{timestamp}</p>
        </div>
        <p>请注意风险控制，谨慎交易。</p>
        <p>TradingAgents 团队</p>
    </body>
    </html>
    """

    # 风险预警模板
    RISK_ALERT = """
    <html>
    <body>
        <h2>⚠️ 风险预警</h2>
        <p>亲爱的用户，</p>
        <p>系统检测到风险情况：</p>
        <div style="background-color: #ffebee; padding: 15px; border-radius: 5px; border-left: 4px solid #f44336;">
            <p><strong>预警类型：</strong>{alert_type}</p>
            <p><strong>涉及股票：</strong>{symbol}</p>
            <p><strong>风险等级：</strong><span style="color: #f44336;">{severity}</span></p>
            <p><strong>预警信息：</strong>{message}</p>
            <p><strong>建议行动：</strong>{suggested_action}</p>
            <p><strong>预警时间：</strong>{timestamp}</p>
        </div>
        <p>请及时关注投资组合风险。</p>
        <p>TradingAgents 团队</p>
    </body>
    </html>
    """

    # 日报模板
    DAILY_REPORT = """
    <html>
    <body>
        <h2>📊 每日交易报告</h2>
        <p>亲爱的用户，</p>
        <p>以下是您今天的交易报告：</p>

        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>💰 账户概览</h4>
            <p><strong>期初价值：</strong>¥{initial_value:,.2f}</p>
            <p><strong>期末价值：</strong>¥{current_value:,.2f}</p>
            <p><strong>当日盈亏：</strong><span style="color: {'green' if daily_pnl >= 0 else 'red'};">{'+' if daily_pnl >= 0 else ''}¥{daily_pnl:,.2f}</span></p>
            <p><strong>盈亏比例：</strong><span style="color: {'green' if daily_pnl >= 0 else 'red'};">{'+' if daily_pnl >= 0 else ''}{daily_pnl_ratio:.2%}</span></p>
        </div>

        <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>📈 交易统计</h4>
            <p><strong>订单数量：</strong>{orders_count}</p>
            <p><strong>持仓数量：</strong>{positions_count}</p>
            <p><strong>预警次数：</strong>{alerts_count}</p>
        </div>

        {positions_html}

        <p>感谢您使用 TradingAgents！</p>
        <p>报告生成时间：{report_time}</p>
    </body>
    </html>
    """

    # 持仓详情模板
    POSITIONS_DETAIL = """
        <div style="background-color: #f3e6f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>📊 持仓详情</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #e1bee7;">
                        <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">股票代码</th>
                        <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">持仓数量</th>
                        <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">平均成本</th>
                        <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">当前价格</th>
                        <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">市值</th>
                        <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">浮动盈亏</th>
                    </tr>
                </thead>
                <tbody>
                    {position_rows}
                </tbody>
            </table>
        </div>
    """

    # 持仓行模板
    POSITION_ROW = """
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">{symbol}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">{quantity}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">¥{average_price:.2f}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">¥{current_price:.2f}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">¥{market_value:,.2f}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd; color: {'green' if unrealized_pnl >= 0 else 'red'};">
                            {'+' if unrealized_pnl >= 0 else ''}¥{unrealized_pnl:,.2f}
                        </td>
                    </tr>
    """


class EmailService:
    """邮件服务"""

    def __init__(self, config: Optional[EmailConfig] = None):
        """
        初始化邮件服务

        Args:
            config: 邮件配置，如果为None则从配置文件读取
        """
        if config is None:
            # 从系统配置读取邮件配置
            system_config = get_config()
            email_config_dict = {
                'enabled': system_config.email_notification.enabled,
                'smtp_server': system_config.email_notification.smtp_server,
                'smtp_port': system_config.email_notification.smtp_port,
                'email_user': system_config.email_notification.email_user,
                'email_password': system_config.email_notification.email_password,
                'use_tls': system_config.email_notification.use_tls,
                'sender_name': system_config.email_notification.sender_name
            }
            config = EmailConfig(**email_config_dict)

        self.config = config
        self.smtp_server = None

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        content: str,
        content_type: str = "html",
        attachments: List[str] = None
    ) -> bool:
        """
        发送邮件

        Args:
            to_emails: 收件人邮箱列表
            subject: 邮件主题
            content: 邮件内容
            content_type: 内容类型 ('html' or 'plain')
            attachments: 附件文件路径列表

        Returns:
            是否发送成功
        """
        try:
            # 创建邮件消息
            msg = MIMEMultipart()
            msg['From'] = formataddr((str(Header(self.config.sender_name, 'utf-8')), self.config.email_user))
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = Header(subject, 'utf-8')

            # 添加邮件内容
            if content_type == "html":
                msg.attach(MIMEText(content, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(content, 'plain', 'utf-8'))

            # 添加附件
            if attachments:
                for attachment_path in attachments:
                    self._add_attachment(msg, attachment_path)

            # 发送邮件
            self._send_smtp_email(msg, to_emails)

            logger.info(f"邮件发送成功: {subject} -> {to_emails}")
            return True

        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False

    def _send_smtp_email(self, msg: MIMEMultipart, to_emails: List[str]):
        """通过SMTP发送邮件"""
        try:
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)

            if self.config.use_tls:
                server.starttls()

            server.login(self.config.email_user, self.config.email_password)
            server.sendmail(self.config.email_user, to_emails, msg.as_string())
            server.quit()

        except Exception as e:
            logger.error(f"SMTP发送失败: {str(e)}")
            raise

    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """添加附件"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename= {os.path.basename(file_path)}"
                )
                msg.attach(part)

        except Exception as e:
            logger.error(f"添加附件失败 {file_path}: {str(e)}")
            raise

    def send_trade_alert(
        self,
        to_emails: List[str],
        symbol: str,
        trade_type: str,
        quantity: int,
        price: float,
        confidence: float,
        timestamp: str
    ) -> bool:
        """发送交易提醒邮件"""
        subject = f"交易提醒 - {symbol} {trade_type}"

        content = EmailTemplate.TRADE_ALERT.format(
            symbol=symbol,
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            confidence=confidence,
            timestamp=timestamp
        )

        return self.send_email(to_emails, subject, content)

    def send_risk_alert(
        self,
        to_emails: List[str],
        alert_type: str,
        symbol: str,
        severity: str,
        message: str,
        suggested_action: str,
        timestamp: str
    ) -> bool:
        """发送风险预警邮件"""
        subject = f"风险预警 - {alert_type} ({severity})"

        content = EmailTemplate.RISK_ALERT.format(
            alert_type=alert_type,
            symbol=symbol,
            severity=severity,
            message=message,
            suggested_action=suggested_action,
            timestamp=timestamp
        )

        return self.send_email(to_emails, subject, content)

    def send_daily_report(
        self,
        to_emails: List[str],
        report_data: Dict[str, Any]
    ) -> bool:
        """发送每日报告邮件"""
        subject = f"每日交易报告 - {report_data.get('date', '今日')}"

        # 生成持仓详情HTML
        positions_html = ""
        if report_data.get('top_positions'):
            position_rows = []
            for pos in report_data['top_positions']:
                position_rows.append(EmailTemplate.POSITION_ROW.format(
                    symbol=pos.get('symbol', ''),
                    quantity=pos.get('quantity', 0),
                    average_price=pos.get('average_price', 0),
                    current_price=pos.get('current_price', 0),
                    market_value=pos.get('market_value', 0),
                    unrealized_pnl=pos.get('unrealized_pnl', 0)
                ))

            positions_html = EmailTemplate.POSITIONS_DETAIL.format(
                position_rows=''.join(position_rows)
            )

        content = EmailTemplate.DAILY_REPORT.format(
            initial_value=report_data.get('initial_value', 0),
            current_value=report_data.get('current_value', 0),
            daily_pnl=report_data.get('daily_pnl', 0),
            daily_pnl_ratio=report_data.get('daily_pnl_ratio', 0),
            orders_count=report_data.get('orders_count', 0),
            positions_count=report_data.get('positions_count', 0),
            alerts_count=report_data.get('alerts_count', 0),
            positions_html=positions_html,
            report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        return self.send_email(to_emails, subject, content)

    def send_system_notification(
        self,
        to_emails: List[str],
        notification_type: str,
        message: str,
        details: Dict = None
    ) -> bool:
        """发送系统通知邮件"""
        subject = f"系统通知 - {notification_type}"

        content = f"""
        <html>
        <body>
            <h2>🔔 系统通知</h2>
            <p>亲爱的用户，</p>
            <p>系统有以下通知：</p>
            <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px;">
                <p><strong>通知类型：</strong>{notification_type}</p>
                <p><strong>消息内容：</strong>{message}</p>
                <p><strong>通知时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            {f'<div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 15px;"><h4>详细信息：</h4><pre>{json.dumps(details, indent=2, ensure_ascii=False)}</pre></div>' if details else ''}

            <p>感谢您使用 TradingAgents！</p>
        </body>
        </html>
        """

        return self.send_email(to_emails, subject, content)

    def test_connection(self) -> bool:
        """测试邮件服务连接"""
        try:
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)

            if self.config.use_tls:
                server.starttls()

            server.login(self.config.email_user, self.config.email_password)

            # 发送测试邮件给自己
            test_content = """
            <html>
            <body>
                <h2>✅ 邮件服务测试</h2>
                <p>邮件服务连接正常！</p>
                <p>测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """

            self.send_email(
                [self.config.email_user],
                "邮件服务测试",
                test_content
            )

            server.quit()
            logger.info("邮件服务测试成功")
            return True

        except Exception as e:
            logger.error(f"邮件服务测试失败: {str(e)}")
            return False


class NotificationManager:
    """通知管理器"""

    def __init__(self, email_service: Optional[EmailService] = None):
        """
        初始化通知管理器

        Args:
            email_service: 邮件服务实例，如果为None则自动创建
        """
        if email_service is None:
            email_service = EmailService()

        self.email_service = email_service

        # 获取系统配置中的通知设置
        system_config = get_config()
        self.notification_settings = system_config.email_notification.notifications.copy()
        self.notification_settings['email_recipients'] = system_config.email_notification.recipients.copy()

    def set_notification_settings(self, settings: Dict[str, Any]):
        """设置通知选项"""
        self.notification_settings.update(settings)

    def add_recipient(self, email: str):
        """添加收件人"""
        if email not in self.notification_settings['email_recipients']:
            self.notification_settings['email_recipients'].append(email)

    def remove_recipient(self, email: str):
        """移除收件人"""
        if email in self.notification_settings['email_recipients']:
            self.notification_settings['email_recipients'].remove(email)

    def send_trade_alert(self, symbol: str, trade_type: str, quantity: int, price: float, confidence: float):
        """发送交易提醒"""
        if not self.notification_settings['trade_alerts']:
            return

        recipients = self.notification_settings['email_recipients']
        if not recipients:
            logger.warning("未设置邮件收件人")
            return

        self.email_service.send_trade_alert(
            recipients,
            symbol,
            trade_type,
            quantity,
            price,
            confidence,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def send_risk_alert(self, alert_type: str, symbol: str, severity: str, message: str, suggested_action: str):
        """发送风险预警"""
        if not self.notification_settings['risk_alerts']:
            return

        recipients = self.notification_settings['email_recipients']
        if not recipients:
            return

        self.email_service.send_risk_alert(
            recipients,
            alert_type,
            symbol,
            severity,
            message,
            suggested_action,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def send_daily_report(self, report_data: Dict[str, Any]):
        """发送每日报告"""
        if not self.notification_settings['daily_reports']:
            return

        recipients = self.notification_settings['email_recipients']
        if not recipients:
            return

        self.email_service.send_daily_report(recipients, report_data)

    def send_system_notification(self, notification_type: str, message: str, details: Dict = None):
        """发送系统通知"""
        if not self.notification_settings['system_notifications']:
            return

        recipients = self.notification_settings['email_recipients']
        if not recipients:
            return

        self.email_service.send_system_notification(
            recipients,
            notification_type,
            message,
            details
        )


# 默认邮件配置
DEFAULT_EMAIL_CONFIG = EmailConfig(
    smtp_server="smtp.qq.com",
    smtp_port=587,
    sender_name="TradingAgents"
)


# 便捷函数
def create_email_service(config: Dict[str, Any] = None) -> EmailService:
    """创建邮件服务实例"""
    email_config = DEFAULT_EMAIL_CONFIG

    if config:
        for key, value in config.items():
            if hasattr(email_config, key):
                setattr(email_config, key, value)

    return EmailService(email_config)


def test_email_config(config: Dict[str, Any]) -> bool:
    """测试邮件配置"""
    try:
        service = create_email_service(config)
        return service.test_connection()
    except Exception as e:
        logger.error(f"邮件配置测试失败: {str(e)}")
        return False