/**
 * TradingAgents 交易看板JavaScript
 * 实现实时数据更新、图表展示、交易管理等功能
 */

// 全局变量
let socket;
let charts = {};
let currentPage = 1;
let pageSize = 20;
let allTrades = [];
let filteredTrades = [];
let refreshTimer = null;

// 初始化函数
function initDashboard() {
    console.log('初始化交易看板...');

    // 连接WebSocket
    connectWebSocket();

    // 初始化图表
    initCharts();

    // 绑定事件监听器
    bindEventListeners();

    // 启动自动刷新
    startAutoRefresh();

    // 加载初始数据
    loadInitialData();
}

// 连接WebSocket
function connectWebSocket() {
    socket = io();

    socket.on('connect', function() {
        console.log('WebSocket连接成功');
        updateConnectionStatus(true);

        // 请求初始数据
        socket.emit('request_update', {type: 'dashboard'});
    });

    socket.on('disconnect', function() {
        console.log('WebSocket连接断开');
        updateConnectionStatus(false);
    });

    // 监听各种数据更新
    socket.on('portfolio_update', function(data) {
        updatePortfolioData(data);
    });

    socket.on('positions_update', function(data) {
        updatePositionsData(data);
    });

    socket.on('trades_update', function(data) {
        updateTradesData(data);
    });

    socket.on('market_update', function(data) {
        updateMarketData(data);
    });

    socket.on('alert_update', function(data) {
        updateAlerts(data);
    });
}

// 更新连接状态
function updateConnectionStatus(connected) {
    const statusEl = document.getElementById('connection-status');
    if (connected) {
        statusEl.innerHTML = '<i class="fas fa-circle text-success me-1"></i>实时连接';
    } else {
        statusEl.innerHTML = '<i class="fas fa-circle text-danger me-1"></i>连接断开';
    }
}

// 初始化图表
function initCharts() {
    console.log('初始化图表...');

    // 盈亏趋势图
    const pnlCtx = document.getElementById('pnl-chart').getContext('2d');
    charts.pnlChart = new Chart(pnlCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '累计盈亏',
                data: [],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#007bff',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return '盈亏: ¥' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: '时间'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: '盈亏金额 (¥)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '¥' + value.toLocaleString();
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'nearest'
            }
        }
    });

    // 持仓分布饼图
    const positionCtx = document.getElementById('position-chart').getContext('2d');
    charts.positionChart = new Chart(positionCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#007bff', '#28a745', '#ffc107', '#fd7e14',
                    '#6f42c1', '#e83e8c', '#20c997', '#6c757d'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ¥${context.parsed.toLocaleString()} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// 绑定事件监听器
function bindEventListeners() {
    // 搜索交易记录
    document.getElementById('search-trade').addEventListener('input', function(e) {
        filterTrades(e.target.value);
    });

    // 时间筛选
    document.getElementById('time-filter').addEventListener('change', function(e) {
        filterTradesByTime(e.target.value);
    });

    // 股票筛选
    document.getElementById('symbol-filter').addEventListener('change', function(e) {
        filterTradesBySymbol(e.target.value);
    });

    // 交易方向筛选
    document.getElementById('side-filter').addEventListener('change', function(e) {
        filterTradesBySide(e.target.value);
    });

    // 分页点击
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            e.preventDefault();
            const page = parseInt(e.target.getAttribute('data-page'));
            if (page) {
                currentPage = page;
                updateTradesTable(filteredTrades);
            }
        }
    });
}

// 启动自动刷新
function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }

    refreshTimer = setInterval(() => {
        socket.emit('request_update', {type: 'dashboard'});
    }, 10000); // 每10秒刷新一次
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
}

// 加载初始数据
function loadInitialData() {
    // 请求所有数据
    socket.emit('request_update', {type: 'all'});
    showLoading();
    setTimeout(hideLoading, 1500);
}

// 更新投资组合数据
function updatePortfolioData(data) {
    console.log('更新投资组合数据:', data);

    // 更新顶部指标
    document.getElementById('portfolio-total').textContent =
        '¥' + data.total_value.toLocaleString('zh-CN', {minimumFractionDigits: 2});

    document.getElementById('daily-pnl').textContent =
        (data.daily_pnl >= 0 ? '+' : '') + '¥' + data.daily_pnl.toLocaleString('zh-CN', {minimumFractionDigits: 2});

    document.getElementById('daily-return').textContent =
        (data.daily_pnl >= 0 ? '+' : '') + ((data.daily_pnl / (data.total_value - data.daily_pnl)) * 100).toFixed(2) + '%';

    document.getElementById('positions-count').textContent = data.positions_count || 0;
}

// 更新持仓数据
function updatePositionsData(data) {
    console.log('更新持仓数据:', data);
    updatePositionsTable(data.positions || []);
    updatePositionChart(data.positions || []);
}

// 更新交易数据
function updateTradesData(data) {
    console.log('更新交易数据:', data);
    allTrades = data.trades || [];
    filteredTrades = allTrades;
    updateTradesTable(filteredTrades);
    updatePnlChart(data.pnl_history || []);
}

// 更新市场数据
function updateMarketData(data) {
    console.log('更新市场数据:', data);

    const container = document.getElementById('market-overview');
    const marketData = data.market_data || {};

    let html = '<div class="row">';
    for (const [symbol, info] of Object.entries(marketData)) {
        const changeClass = info.change >= 0 ? 'text-success' : 'text-danger';
        html += `
            <div class="col-md-6 mb-2">
                <div class="d-flex justify-content-between align-items-center p-2 bg-light rounded">
                    <div>
                        <div class="fw-bold">${symbol}</div>
                        <small class="text-muted">${info.name || ''}</small>
                    </div>
                    <div class="text-end">
                        <div class="fw-bold">¥${info.price}</div>
                        <small class="${changeClass}">
                            ${info.change >= 0 ? '+' : ''}${info.change} (${info.change_percent}%)
                        </small>
                    </div>
                </div>
            </div>
        `;
    }
    html += '</div>';
    container.innerHTML = html;
}

// 更新预警信息
function updateAlerts(data) {
    console.log('更新预警信息:', data);
    // 实现预警显示逻辑
}

// 更新持仓表格
function updatePositionsTable(positions) {
    const tbody = document.getElementById('positions-tbody');
    tbody.innerHTML = '';

    if (!positions || positions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">暂无持仓数据</td></tr>';
        return;
    }

    positions.forEach(position => {
        const pnlClass = position.unrealized_pnl >= 0 ? 'positive' : 'negative';
        const pnlIcon = position.unrealized_pnl >= 0 ? 'up' : 'down';
        const pnlPercent = position.market_value > 0 ?
            (position.unrealized_pnl / position.market_value * 100).toFixed(2) : '0.00';

        const row = document.createElement('tr');
        row.className = 'fade-in';
        row.innerHTML = `
            <td>
                <div class="fw-bold">${position.symbol}</div>
                <small class="text-muted">${position.name || ''}</small>
            </td>
            <td>${position.quantity.toLocaleString()}</td>
            <td>¥${position.average_price.toFixed(2)}</td>
            <td>¥${position.current_price.toFixed(2)}</td>
            <td>¥${position.market_value.toLocaleString()}</td>
            <td class="position-profit ${pnlClass}">
                <i class="fas fa-arrow-${pnlIcon} me-1"></i>
                ¥${Math.abs(position.unrealized_pnl).toLocaleString()}
            </td>
            <td class="${pnlClass}">
                ${position.unrealized_pnl >= 0 ? '+' : ''}${pnlPercent}%
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewPositionDetail('${position.symbol}')" title="详情">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="addToPosition('${position.symbol}')" title="加仓">
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="sellPosition('${position.symbol}')" title="卖出">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// 更新交易表格
function updateTradesTable(trades) {
    const tbody = document.getElementById('trades-tbody');
    tbody.innerHTML = '';

    if (!trades || trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center text-muted py-4">暂无交易记录</td></tr>';
        return;
    }

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, trades.length);
    const pageTrades = trades.slice(startIndex, endIndex);

    pageTrades.forEach((trade, index) => {
        const pnlClass = trade.pnl >= 0 ? 'positive' : 'negative';
        const sideClass = trade.side === 'buy' ? 'success' : 'danger';
        const statusClass = trade.status === 'filled' ? 'success' : 'warning';

        const row = document.createElement('tr');
        row.className = 'fade-in';
        row.innerHTML = `
            <td>${new Date(trade.timestamp).toLocaleString('zh-CN')}</td>
            <td>
                <span class="fw-bold">${trade.symbol}</span>
            </td>
            <td>
                <span class="badge badge-${sideClass}">${trade.side === 'buy' ? '买入' : '卖出'}</span>
            </td>
            <td>${trade.quantity.toLocaleString()}</td>
            <td>¥${trade.price.toFixed(2)}</td>
            <td>¥${(trade.quantity * trade.price).toLocaleString()}</td>
            <td>¥${trade.commission.toFixed(2)}</td>
            <td class="${pnlClass}">
                ${trade.pnl >= 0 ? '+' : ''}¥${Math.abs(trade.pnl).toLocaleString()}
            </td>
            <td>
                <span class="badge badge-${statusClass}">${trade.status}</span>
            </td>
            <td>
                <small class="text-muted">${trade.operator || '系统'}</small>
            </td>
        `;
        tbody.appendChild(row);
    });

    // 更新分页
    updatePagination(trades.length);
}

// 更新分页
function updatePagination(totalItems) {
    const totalPages = Math.ceil(totalItems / pageSize);
    const pagination = document.getElementById('trades-pagination');
    pagination.innerHTML = '';

    if (totalPages <= 1) return;

    // 上一页
    if (currentPage > 1) {
        pagination.innerHTML += `<li class="page-item"><a class="page-link" href="#" data-page="${currentPage - 1}">上一页</a></li>`;
    }

    // 页码
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        pagination.innerHTML += `<li class="page-item ${activeClass}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
    }

    // 下一页
    if (currentPage < totalPages) {
        pagination.innerHTML += `<li class="page-item"><a class="page-link" href="#" data-page="${currentPage + 1}">下一页</a></li>`;
    }
}

// 更新持仓分布图表
function updatePositionChart(positions) {
    if (!charts.positionChart || !positions) return;

    const labels = positions.map(pos => pos.symbol);
    const data = positions.map(pos => pos.market_value);

    charts.positionChart.data.labels = labels;
    charts.positionChart.data.datasets[0].data = data;
    charts.positionChart.update();
}

// 更新盈亏趋势图表
function updatePnlChart(pnlHistory) {
    if (!charts.pnlChart || !pnlHistory) return;

    const labels = pnlHistory.map(item => item.time);
    const data = pnlHistory.map(item => item.pnl);

    charts.pnlChart.data.labels = labels;
    charts.pnlChart.data.datasets[0].data = data;
    charts.pnlChart.update();
}

// 筛选交易记录
function filterTrades(searchTerm) {
    if (!searchTerm) {
        filteredTrades = allTrades;
    } else {
        filteredTrades = allTrades.filter(trade =>
            trade.symbol.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }
    currentPage = 1;
    updateTradesTable(filteredTrades);
}

// 按时间筛选
function filterTradesByTime(timeRange) {
    const now = new Date();
    let startDate;

    switch(timeRange) {
        case 'today':
            startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            break;
        case 'week':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1);
            break;
        default:
            filteredTrades = allTrades;
            updateTradesTable(filteredTrades);
            return;
    }

    filteredTrades = allTrades.filter(trade => new Date(trade.timestamp) >= startDate);
    currentPage = 1;
    updateTradesTable(filteredTrades);
}

// 按股票筛选
function filterTradesBySymbol(symbol) {
    if (!symbol) {
        filteredTrades = allTrades;
    } else {
        filteredTrades = allTrades.filter(trade => trade.symbol === symbol);
    }
    currentPage = 1;
    updateTradesTable(filteredTrades);
}

// 按交易方向筛选
function filterTradesBySide(side) {
    if (!side) {
        filteredTrades = allTrades;
    } else {
        filteredTrades = allTrades.filter(trade => trade.side === side);
    }
    currentPage = 1;
    updateTradesTable(filteredTrades);
}

// 查看持仓详情
function viewPositionDetail(symbol) {
    console.log('查看持仓详情:', symbol);
    // 实现持仓详情模态框
}

// 加仓操作
function addToPosition(symbol) {
    const quantity = prompt(`请输入加仓数量 (${symbol}):`);
    if (quantity && parseInt(quantity) > 0) {
        // 发送加仓请求
        fetch('/api/trade', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                quantity: parseInt(quantity),
                side: 'buy',
                order_type: 'market'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('加仓订单提交成功');
                socket.emit('request_update', {type: 'positions'});
            } else {
                alert('加仓失败: ' + data.error);
            }
        })
        .catch(error => {
            console.error('加仓请求失败:', error);
            alert('加仓请求失败');
        });
    }
}

// 卖出操作
function sellPosition(symbol) {
    if (confirm(`确定要卖出 ${symbol} 的全部持仓吗？`)) {
        // 获取持仓数量
        fetch(`/api/positions`)
            .then(response => response.json())
            .then(data => {
                const position = data.positions.find(p => p.symbol === symbol);
                if (position) {
                    // 发送卖出请求
                    return fetch('/api/trade', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            symbol: symbol,
                            quantity: position.quantity,
                            side: 'sell',
                            order_type: 'market'
                        })
                    });
                } else {
                    throw new Error('未找到持仓信息');
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('卖出订单提交成功');
                    socket.emit('request_update', {type: 'positions'});
                } else {
                    alert('卖出失败: ' + data.error);
                }
            })
            .catch(error => {
                console.error('卖出请求失败:', error);
                alert('卖出请求失败');
            });
    }
}

// 导出交易记录
function exportTrades() {
    const data = filteredTrades.length > 0 ? filteredTrades : allTrades;

    if (data.length === 0) {
        alert('没有交易记录可供导出');
        return;
    }

    // 转换为CSV格式
    const headers = ['交易时间', '股票代码', '交易方向', '数量', '价格', '金额', '手续费', '盈亏', '状态', '操作员'];
    const csvContent = [
        headers.join(','),
        ...data.map(trade => [
            new Date(trade.timestamp).toLocaleString('zh-CN'),
            trade.symbol,
            trade.side === 'buy' ? '买入' : '卖出',
            trade.quantity,
            trade.price,
            trade.quantity * trade.price,
            trade.commission,
            trade.pnl,
            trade.status,
            trade.operator || '系统'
        ].join(','))
    ].join('\n');

    // 下载CSV文件
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `交易记录_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// 显示加载状态
function showLoading() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

// 隐藏加载状态
function hideLoading() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) modal.hide();
}

// 系统控制函数
function startTrading() {
    fetch('/api/control/start')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('交易系统启动成功');
            } else {
                alert('启动失败: ' + data.error);
            }
        })
        .catch(error => {
            console.error('启动请求失败:', error);
            alert('启动请求失败');
        });
}

function pauseTrading() {
    fetch('/api/control/stop')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('交易系统已暂停');
            } else {
                alert('暂停失败: ' + data.error);
            }
        })
        .catch(error => {
            console.error('暂停请求失败:', error);
            alert('暂停请求失败');
        });
}

function generateReport() {
    showLoading();
    fetch('/api/report/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            report_type: 'daily',
            format: 'html'
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            // 显示报告内容
            document.getElementById('trade-detail-content').innerHTML = data.report_html;
            new bootstrap.Modal(document.getElementById('tradeDetailModal')).show();
        } else {
            alert('生成报告失败: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading();
        console.error('生成报告请求失败:', error);
        alert('生成报告请求失败');
    });
}

function viewAnalysis() {
    window.location.href = '/analysis';
}

// 更新概览卡片数据
function updateSummaryCards(data) {
    document.getElementById('today-trades').textContent = data.today_trades || '0';
    document.getElementById('win-rate').textContent = data.win_rate || '0%';
    document.getElementById('avg-profit').textContent =
        (data.avg_profit >= 0 ? '+' : '') + '¥' + Math.abs(data.avg_profit || 0).toFixed(2);
    document.getElementById('max-drawdown').textContent = data.max_drawdown || '0%';
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('交易看板页面加载完成');
    initDashboard();
});

// 页面卸载时清理
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
    if (socket) {
        socket.disconnect();
    }
});