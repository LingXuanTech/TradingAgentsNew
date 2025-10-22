"""
自动化交易调度器模块
负责定时执行各种交易相关任务
"""

import logging
from datetime import datetime, time
from typing import Dict, List, Callable, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from zoneinfo import ZoneInfo

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingScheduler:
    """自动化交易任务调度器"""

    def __init__(self, timezone: str = "Asia/Shanghai"):
        """
        初始化调度器

        Args:
            timezone: 时区设置，默认为Asia/Shanghai
        """
        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.timezone = ZoneInfo(timezone)
        self.tasks: Dict[str, Dict] = {}
        self.is_running = False

        # 交易时间配置
        self.market_open = time(9, 30)   # 开盘时间
        self.market_close = time(15, 0)  # 收盘时间
        self.lunch_break_start = time(11, 30)  # 午休开始
        self.lunch_break_end = time(13, 0)     # 午休结束

    def add_market_analysis_task(
        self,
        task_func: Callable,
        interval_minutes: int = 30,
        task_name: str = "market_analysis"
    ):
        """
        添加市场分析任务

        Args:
            task_func: 任务执行函数
            interval_minutes: 执行间隔（分钟）
            task_name: 任务名称
        """
        # 只在交易时间内执行
        trigger = IntervalTrigger(
            minutes=interval_minutes,
            start_date=f"09:30:00",
            end_date=f"15:00:00"
        )

        self._add_task(
            task_name=task_name,
            task_func=task_func,
            trigger=trigger,
            description=f"市场分析任务，每{interval_minutes}分钟执行一次"
        )

    def add_portfolio_check_task(
        self,
        task_func: Callable,
        interval_minutes: int = 5,
        task_name: str = "portfolio_check"
    ):
        """
        添加持仓检查任务

        Args:
            task_func: 任务执行函数
            interval_minutes: 执行间隔（分钟）
            task_name: 任务名称
        """
        trigger = IntervalTrigger(minutes=interval_minutes)

        self._add_task(
            task_name=task_name,
            task_func=task_func,
            trigger=trigger,
            description=f"持仓风险检查，每{interval_minutes}分钟执行一次"
        )

    def add_daily_report_task(
        self,
        task_func: Callable,
        report_time: str = "15:30",
        task_name: str = "daily_report"
    ):
        """
        添加每日报告任务

        Args:
            task_func: 任务执行函数
            report_time: 报告生成时间，格式"HH:MM"
            task_name: 任务名称
        """
        trigger = CronTrigger(hour=report_time.split(':')[0], minute=report_time.split(':')[1])

        self._add_task(
            task_name=task_name,
            task_func=task_func,
            trigger=trigger,
            description=f"每日交易报告，{report_time}生成"
        )

    def add_weekly_analysis_task(
        self,
        task_func: Callable,
        weekly_day: str = "fri",
        analysis_time: str = "16:00",
        task_name: str = "weekly_analysis"
    ):
        """
        添加每周分析任务

        Args:
            task_func: 任务执行函数
            weekly_day: 每周执行的日子，默认为周五
            analysis_time: 执行时间
            task_name: 任务名称
        """
        day_map = {
            'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
            'fri': 4, 'sat': 5, 'sun': 6
        }

        trigger = CronTrigger(
            day_of_week=day_map[weekly_day],
            hour=analysis_time.split(':')[0],
            minute=analysis_time.split(':')[1]
        )

        self._add_task(
            task_name=task_name,
            task_func=task_func,
            trigger=trigger,
            description=f"每周分析报告，每周{weekly_day} {analysis_time}执行"
        )

    def _add_task(
        self,
        task_name: str,
        task_func: Callable,
        trigger: Any,
        description: str
    ):
        """内部方法：添加任务到调度器"""
        try:
            self.scheduler.add_job(
                func=task_func,
                trigger=trigger,
                id=task_name,
                name=description,
                replace_existing=True
            )

            self.tasks[task_name] = {
                'function': task_func,
                'trigger': trigger,
                'description': description,
                'enabled': True
            }

            logger.info(f"任务 '{task_name}' 已添加到调度器: {description}")

        except Exception as e:
            logger.error(f"添加任务 '{task_name}' 失败: {str(e)}")
            raise

    def start(self):
        """启动调度器"""
        if not self.is_running:
            try:
                self.scheduler.start()
                self.is_running = True
                logger.info("交易调度器已启动")

                # 打印所有活跃任务
                self._print_active_jobs()

            except Exception as e:
                logger.error(f"启动调度器失败: {str(e)}")
                raise
        else:
            logger.warning("调度器已经在运行中")

    def stop(self):
        """停止调度器"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("交易调度器已停止")
        else:
            logger.warning("调度器未在运行")

    def pause_task(self, task_name: str):
        """暂停指定任务"""
        try:
            self.scheduler.pause_job(task_name)
            if task_name in self.tasks:
                self.tasks[task_name]['enabled'] = False
            logger.info(f"任务 '{task_name}' 已暂停")
        except Exception as e:
            logger.error(f"暂停任务 '{task_name}' 失败: {str(e)}")

    def resume_task(self, task_name: str):
        """恢复指定任务"""
        try:
            self.scheduler.resume_job(task_name)
            if task_name in self.tasks:
                self.tasks[task_name]['enabled'] = True
            logger.info(f"任务 '{task_name}' 已恢复")
        except Exception as e:
            logger.error(f"恢复任务 '{task_name}' 失败: {str(e)}")

    def remove_task(self, task_name: str):
        """删除指定任务"""
        try:
            self.scheduler.remove_job(task_name)
            if task_name in self.tasks:
                del self.tasks[task_name]
            logger.info(f"任务 '{task_name}' 已删除")
        except Exception as e:
            logger.error(f"删除任务 '{task_name}' 失败: {str(e)}")

    def get_task_status(self, task_name: str) -> Dict:
        """获取任务状态"""
        job = self.scheduler.get_job(task_name)
        if job:
            return {
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time,
                'enabled': not job.next_run_time is None if hasattr(job, 'next_run_time') else True
            }
        return None

    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        return [
            {
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time,
                'enabled': job.next_run_time is not None
            }
            for job in self.scheduler.get_jobs()
        ]

    def _print_active_jobs(self):
        """打印活跃任务信息"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            logger.info(f"当前活跃任务数量: {len(jobs)}")
            for job in jobs:
                logger.info(f"  - {job.id}: {job.name}")
                if hasattr(job, 'next_run_time') and job.next_run_time:
                    logger.info(f"    下次执行时间: {job.next_run_time}")
        else:
            logger.info("暂无活跃任务")

    def is_market_open(self) -> bool:
        """判断当前是否为交易时间"""
        now = datetime.now(self.timezone).time()

        # 检查是否在交易时间内
        if not (self.market_open <= now <= self.market_close):
            return False

        # 检查是否在午休时间
        if self.lunch_break_start <= now <= self.lunch_break_end:
            return False

        return True

    def get_next_market_open(self) -> datetime:
        """获取下次开盘时间"""
        now = datetime.now(self.timezone)
        next_open = now.replace(
            hour=self.market_open.hour,
            minute=self.market_open.minute,
            second=0,
            microsecond=0
        )

        # 如果当前时间已经过了今天的开盘时间，则计算下一天的
        if now.time() >= self.market_open:
            next_open = next_open.replace(day=next_open.day + 1)

        return next_open


# 全局调度器实例
trading_scheduler = TradingScheduler()