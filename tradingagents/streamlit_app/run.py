#!/usr/bin/env python3
"""
TradingAgents Streamlit前端启动脚本
启动现代化的Web界面，支持实时数据展示和交互操作
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_streamlit_app():
    """启动Streamlit应用"""
    try:
        # 设置环境变量
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

        logger.info("启动TradingAgents Streamlit前端...")
        logger.info("访问地址: http://localhost:8501")
        logger.info("按 Ctrl+C 停止服务")

        # 使用streamlit命令行运行应用
        app_path = Path(__file__).parent / "app.py"
        subprocess.run(["streamlit", "run", str(app_path)], check=True)

    except KeyboardInterrupt:
        logger.info("用户中断，正在停止服务...")
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        sys.exit(1)


def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        'streamlit',
        'streamlit-shadcn-ui',
        'plotly',
        'pandas',
        'numpy'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        logger.error(f"缺少必要依赖包: {', '.join(missing_packages)}")
        logger.info("请运行以下命令安装依赖:")
        logger.info("pip install -r requirements.txt")
        return False

    return True


def main():
    """主函数"""
    print("🚀 TradingAgents Streamlit前端启动器")
    print("=" * 50)

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 检查配置文件
    config_file = project_root / 'config' / 'user_config.yaml'
    if not config_file.exists():
        logger.warning("未找到用户配置文件，建议复制配置模板")
        logger.info("cp tradingagents/config/user_config_template.yaml tradingagents/config/user_config.yaml")

    # 启动应用
    run_streamlit_app()


if __name__ == "__main__":
    main()