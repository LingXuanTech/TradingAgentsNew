"""
TradingAgents Web管理界面
提供实时监控、交易控制、风险管理等功能
"""

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import threading
import time

# 导入配置管理器
from ..config.config_manager import get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tradingagents_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局状态
class TradingDashboard:
    """交易仪表板状态管理"""

    def __init__(self):
        self.connected_clients = 0
        self.system_status = "stopped"
        self.portfolio_value = 100000.0
        self.daily_pnl = 0.0
        self.positions = []
        self.recent_orders = []
        self.alerts = []
        self.market_data = {}

dashboard = TradingDashboard()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard_page():
    """仪表板页面"""
    return render_template('dashboard.html')


@app.route('/trading')
def trading_page():
    """交易控制页面"""
    return render_template('trading.html')


@app.route('/risk')
def risk_page():
    """风险管理页面"""
    return render_template('risk.html')


@app.route('/analysis')
def analysis_page():
    """技术分析页面"""
    return render_template('analysis.html')


@app.route('/settings')
def settings_page():
    """设置页面"""
    return render_template('settings.html')


# API路由
@app.route('/api/status')
def get_status():
    """获取系统状态"""
    return jsonify({
        'status': dashboard.system_status,
        'portfolio_value': dashboard.portfolio_value,
        'daily_pnl': dashboard.daily_pnl,
        'positions_count': len(dashboard.positions),
        'orders_count': len(dashboard.recent_orders),
        'alerts_count': len(dashboard.alerts),
        'connected_clients': dashboard.connected_clients,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/portfolio')
def get_portfolio():
    """获取投资组合信息"""
    return jsonify({
        'total_value': dashboard.portfolio_value,
        'daily_pnl': dashboard.daily_pnl,
        'positions': dashboard.positions,
        'cash': dashboard.portfolio_value - sum(pos.get('market_value', 0) for pos in dashboard.positions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/positions')
def get_positions():
    """获取持仓信息"""
    return jsonify({
        'positions': dashboard.positions,
        'total_positions': len(dashboard.positions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/orders')
def get_orders():
    """获取订单信息"""
    return jsonify({
        'orders': dashboard.recent_orders,
        'total_orders': len(dashboard.recent_orders),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/alerts')
def get_alerts():
    """获取预警信息"""
    return jsonify({
        'alerts': dashboard.alerts,
        'total_alerts': len(dashboard.alerts),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/market')
def get_market_data():
    """获取市场数据"""
    return jsonify({
        'market_data': dashboard.market_data,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/trade', methods=['POST'])
def place_trade():
    """执行交易"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        side = data.get('side')
        order_type = data.get('order_type', 'market')

        # 这里应该调用真实的交易接口
        # 目前返回模拟结果
        order_id = f"ORDER_{int(time.time())}"

        order_info = {
            'order_id': order_id,
            'symbol': symbol,
            'quantity': quantity,
            'side': side,
            'order_type': order_type,
            'status': 'pending',
            'timestamp': datetime.now().isoformat()
        }

        dashboard.recent_orders.insert(0, order_info)

        # 发送实时更新
        socketio.emit('order_update', order_info)

        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': '订单已提交'
        })

    except Exception as e:
        logger.error(f"交易执行失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/control/<action>')
def system_control(action):
    """系统控制"""
    if action == 'start':
        dashboard.system_status = "running"
        socketio.emit('system_status', {'status': 'running'})
        return jsonify({'success': True, 'message': '系统已启动'})

    elif action == 'stop':
        dashboard.system_status = "stopped"
        socketio.emit('system_status', {'status': 'stopped'})
        return jsonify({'success': True, 'message': '系统已停止'})

    elif action == 'restart':
        dashboard.system_status = "restarting"
        socketio.emit('system_status', {'status': 'restarting'})

        # 模拟重启过程
        def delayed_start():
            time.sleep(2)
            dashboard.system_status = "running"
            socketio.emit('system_status', {'status': 'running'})

        threading.Thread(target=delayed_start, daemon=True).start()
        return jsonify({'success': True, 'message': '系统重启中'})

    else:
        return jsonify({'success': False, 'error': '未知操作'}), 400


# SocketIO事件处理
@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    dashboard.connected_clients += 1
    logger.info(f"客户端连接，当前连接数: {dashboard.connected_clients}")
    emit('status', {
        'message': '连接成功',
        'clients': dashboard.connected_clients,
        'timestamp': datetime.now().isoformat()
    })


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接"""
    dashboard.connected_clients = max(0, dashboard.connected_clients - 1)
    logger.info(f"客户端断开，当前连接数: {dashboard.connected_clients}")


@socketio.on('request_update')
def handle_request_update(data):
    """客户端请求数据更新"""
    update_type = data.get('type', 'all')

    if update_type == 'all' or update_type == 'status':
        emit('status_update', get_status().get_json())

    if update_type == 'all' or update_type == 'portfolio':
        emit('portfolio_update', get_portfolio().get_json())

    if update_type == 'all' or update_type == 'orders':
        emit('orders_update', get_orders().get_json())

    if update_type == 'all' or update_type == 'alerts':
        emit('alerts_update', get_alerts().get_json())


def simulate_market_data():
    """模拟市场数据更新"""
    symbols = ['AAPL', 'GOOGL', 'MSFT', '000858.SZ', '600519.SS']

    while True:
        try:
            for symbol in symbols:
                # 模拟价格波动
                base_price = 100.0 if symbol.startswith(('0', '6')) else 150.0
                price_change = (np.random.random() - 0.5) * 2  # -1到1之间的随机数
                current_price = base_price + price_change

                dashboard.market_data[symbol] = {
                    'price': round(current_price, 2),
                    'change': round(price_change, 2),
                    'change_percent': round(price_change / base_price * 100, 2),
                    'volume': np.random.randint(10000, 100000),
                    'timestamp': datetime.now().isoformat()
                }

            # 发送实时更新
            socketio.emit('market_update', {
                'market_data': dashboard.market_data,
                'timestamp': datetime.now().isoformat()
            })

            time.sleep(5)  # 每5秒更新一次

        except Exception as e:
            logger.error(f"模拟市场数据失败: {str(e)}")
            time.sleep(5)


def simulate_portfolio_updates():
    """模拟投资组合更新"""
    while True:
        try:
            # 模拟投资组合价值变化
            change = (np.random.random() - 0.5) * 1000  # -500到500之间的随机数
            dashboard.portfolio_value += change
            dashboard.daily_pnl += change * 0.1  # 模拟日内盈亏

            # 模拟持仓数据
            dashboard.positions = [
                {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'average_price': 150.0,
                    'current_price': 152.0 + (np.random.random() - 0.5) * 10,
                    'market_value': 15200.0,
                    'unrealized_pnl': 200.0
                },
                {
                    'symbol': 'GOOGL',
                    'quantity': 50,
                    'average_price': 2500.0,
                    'current_price': 2520.0 + (np.random.random() - 0.5) * 50,
                    'market_value': 126000.0,
                    'unrealized_pnl': 1000.0
                }
            ]

            # 发送更新
            socketio.emit('portfolio_update', get_portfolio().get_json())

            time.sleep(10)  # 每10秒更新一次

        except Exception as e:
            logger.error(f"模拟投资组合更新失败: {str(e)}")
            time.sleep(10)


def run_web_server(host=None, port=None, debug=None):
    """
    启动Web服务器

    Args:
        host: 监听地址，如果为None则从配置读取
        port: 监听端口，如果为None则从配置读取
        debug: 是否调试模式，如果为None则从配置读取
    """
    # 获取配置
    config = get_config()
    web_config = config.web_interface

    # 使用传入参数或配置值
    server_host = host or web_config.host
    server_port = port or web_config.port
    server_debug = debug if debug is not None else web_config.debug

    # 启动模拟数据线程
    market_thread = threading.Thread(target=simulate_market_data, daemon=True)
    portfolio_thread = threading.Thread(target=simulate_portfolio_updates, daemon=True)

    market_thread.start()
    portfolio_thread.start()

    logger.info(f"启动Web服务器: http://{server_host}:{server_port}")

    # 运行Flask应用
    socketio.run(
        app,
        host=server_host,
        port=server_port,
        debug=server_debug,
        use_reloader=False  # 禁用重载器，避免重复启动
    )


if __name__ == '__main__':
    run_web_server()