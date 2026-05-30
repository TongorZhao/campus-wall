#!/bin/bash
#============================================================
# 校园墙 (Campus Wall) 部署脚本
# 用法: bash deploy.sh [选项]
#   无参数      - 交互式部署
#   --force     - 跳过确认直接部署
#   --restart   - 仅重启服务
#   --check     - 仅检查状态
#============================================================

set -e

# ========== 配置 ==========
PROJECT_DIR="/www/wwwroot/campus-wall"
VENV_DIR="$PROJECT_DIR/venv"
BACKUP_DIR="/www/backup/campus-wall"
SERVICE_NAME="campus-wall"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"
GUNICORN_PID_FILE="/tmp/gunicorn.pid"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ========== 工具函数 ==========
log_info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "${BLUE}[STEP]${NC} $1"; }

confirm() {
    if [[ "$1" == "--force" ]]; then
        return 0
    fi
    read -p "$(echo -e ${YELLOW}$1 [y/N]: ${NC})" -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# ========== 检查函数 ==========
check_status() {
    log_step "========== 服务状态检查 =========="

    # 检查 Django
    if cd "$PROJECT_DIR" && $PYTHON manage.py check --deploy 2>/dev/null | grep -q "System check identified no issues"; then
        log_info "Django 系统检查: ✅ 通过"
    else
        log_warn "Django 系统检查: ⚠️ 有问题"
    fi

    # 检查数据库
    if $PYTHON -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT 1')
print('OK')
" 2>/dev/null | grep -q "OK"; then
        log_info "数据库连接: ✅ 正常"
    else
        log_error "数据库连接: ❌ 失败"
    fi

    # 检查 Gunicorn
    if pgrep -f "gunicorn.*config.wsgi" > /dev/null 2>&1; then
        PID=$(pgrep -f "gunicorn.*config.wsgi" | head -1)
        log_info "Gunicorn 进程: ✅ 运行中 (PID: $PID)"
    else
        log_error "Gunicorn 进程: ❌ 未运行"
    fi

    # 检查端口
    if ss -tlnp | grep -q ":8000 "; then
        log_info "端口 8000: ✅ 监听中"
    else
        log_error "端口 8000: ❌ 未监听"
    fi

    # 检查 .env
    if [[ -f "$PROJECT_DIR/.env" ]]; then
        log_info ".env 文件: ✅ 存在"
    else
        log_warn ".env 文件: ⚠️ 不存在"
    fi

    # 检查 Redis
    if redis-cli ping 2>/dev/null | grep -q "PONG"; then
        log_info "Redis: ✅ 运行中"
    else
        log_warn "Redis: ⚠️ 未运行 (Channels 功能不可用)"
    fi

    # 检查媒体文件
    if [[ -d "$PROJECT_DIR/media" ]]; then
        MEDIA_COUNT=$(find "$PROJECT_DIR/media" -type f | wc -l)
        log_info "媒体文件: ✅ ${MEDIA_COUNT} 个文件"
    else
        log_warn "媒体文件: ⚠️ media/ 目录不存在"
    fi

    echo ""
    log_step "========== 检查完成 =========="
}

# ========== 备份函数 ==========
backup() {
    log_step "备份当前代码..."
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"

    # 只备份代码文件，排除敏感目录
    tar -czf "$BACKUP_PATH.tar.gz" \
        --exclude='venv' \
        --exclude='media' \
        --exclude='staticfiles' \
        --exclude='*.pyc' \
        --exclude='__pycache__' \
        --exclude='.env' \
        --exclude='node_modules' \
        -C "$(dirname $PROJECT_DIR)" "$(basename $PROJECT_DIR)" 2>/dev/null

    log_info "备份完成: $BACKUP_PATH.tar.gz"

    # 保留最近 5 个备份
    ls -t "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
    log_info "已清理旧备份（保留最近5个）"
}

# ========== 部署函数 ==========
deploy() {
    echo ""
    log_step "========== 开始部署 =========="
    echo ""

    # 1. 备份
    if confirm "是否备份当前代码？" "$1"; then
        backup
    fi

    # 2. 更新代码
    log_step "检查代码更新..."
    if [[ -d "$PROJECT_DIR/.git" ]]; then
        log_info "检测到 Git 仓库，使用 git pull"
        cd "$PROJECT_DIR"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || {
            log_warn "Git pull 失败，尝试从远程更新..."
        }
    else
        log_warn "未检测到 Git 仓库，请手动上传代码文件"
        log_warn "确保已覆盖以下文件："
        echo "  - apps/ 目录 (Python 代码)"
        echo "  - templates/ 目录 (模板文件)"
        echo "  - static/ 目录 (静态资源)"
        echo "  - config/ 目录 (配置文件)"
        echo "  - requirements.txt"
        echo ""
        read -p "代码已更新完成？按回车继续..." -r
    fi

    # 3. 检查 .env
    if [[ ! -f "$PROJECT_DIR/.env" ]]; then
        log_error ".env 文件不存在！请先创建 .env 文件"
        exit 1
    fi

    # 4. 安装依赖
    log_step "安装 Python 依赖..."
    if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
        $PIP install -r "$PROJECT_DIR/requirements.txt" -q 2>&1 | tail -3
        log_info "依赖安装完成"
    else
        log_warn "requirements.txt 不存在，跳过依赖安装"
    fi

    # 5. 数据库迁移
    log_step "检查数据库迁移..."
    cd "$PROJECT_DIR"
    MIGRATIONS_PENDING=$($PYTHON manage.py showmigrations --plan 2>/dev/null | grep "\[ \]" | wc -l)
    if [[ $MIGRATIONS_PENDING -gt 0 ]]; then
        log_warn "发现 $MIGRATIONS_PENDING 个未执行的迁移"
        if confirm "是否执行数据库迁移？"; then
            log_step "执行数据库迁移..."
            $PYTHON manage.py migrate
            log_info "数据库迁移完成"
        fi
    else
        log_info "数据库迁移: ✅ 全部已应用"
    fi

    # 6. 收集静态文件
    log_step "收集静态文件..."
    $PYTHON manage.py collectstatic --noinput 2>&1 | tail -3
    log_info "静态文件收集完成"

    # 7. 初始化分类（如果需要）
    if confirm "是否重新初始化分类？（不会覆盖已有分类）" "$1"; then
        $PYTHON manage.py init_categories
    fi

    # 8. 检查系统
    log_step "运行 Django 系统检查..."
    $PYTHON manage.py check 2>&1 | tail -3

    # 9. 重启服务
    log_step "重启 Gunicorn..."
    # 停止旧进程
    if pgrep -f "gunicorn.*config.wsgi" > /dev/null 2>&1; then
        pkill -f "gunicorn.*config.wsgi"
        sleep 2
        log_info "已停止旧的 Gunicorn 进程"
    fi

    # 启动新进程
    cd "$PROJECT_DIR"
    nohup $VENV_DIR/bin/gunicorn config.wsgi:application \
        -b 0.0.0.0:8000 \
        -w 4 \
        --timeout 120 \
        --access-logfile /www/wwwlogs/campus-wall-access.log \
        --error-logfile /www/wwwlogs/campus-wall-error.log \
        --pid /tmp/gunicorn.pid \
        > /dev/null 2>&1 &

    sleep 2

    # 验证启动
    if pgrep -f "gunicorn.*config.wsgi" > /dev/null 2>&1; then
        PID=$(pgrep -f "gunicorn.*config.wsgi" | head -1)
        log_info "Gunicorn 启动成功 ✅ (PID: $PID)"
    else
        log_error "Gunicorn 启动失败 ❌"
        log_error "请查看日志: tail -50 /www/wwwlogs/campus-wall-error.log"
        exit 1
    fi

    # 10. 健康检查
    log_step "健康检查..."
    sleep 1
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ 2>/dev/null)
    if [[ "$HTTP_CODE" == "200" ]]; then
        log_info "HTTP 响应: ✅ $HTTP_CODE OK"
    else
        log_warn "HTTP 响应: ⚠️ $HTTP_CODE"
    fi

    echo ""
    log_step "========== 部署完成 =========="
    echo ""
    log_info "网站地址: http://<your-domain>"
    log_info "后台地址: http://<your-domain>/admin/"
    echo ""
}

# ========== 重启函数 ==========
restart() {
    log_step "重启 Gunicorn..."

    if pgrep -f "gunicorn.*config.wsgi" > /dev/null 2>&1; then
        pkill -f "gunicorn.*config.wsgi"
        sleep 2
    fi

    cd "$PROJECT_DIR"
    nohup $VENV_DIR/bin/gunicorn config.wsgi:application \
        -b 0.0.0.0:8000 \
        -w 4 \
        --timeout 120 \
        --access-logfile /www/wwwlogs/campus-wall-access.log \
        --error-logfile /www/wwwlogs/campus-wall-error.log \
        --pid /tmp/gunicorn.pid \
        > /dev/null 2>&1 &

    sleep 2

    if pgrep -f "gunicorn.*config.wsgi" > /dev/null 2>&1; then
        PID=$(pgrep -f "gunicorn.*config.wsgi" | head -1)
        log_info "Gunicorn 重启成功 ✅ (PID: $PID)"
    else
        log_error "Gunicorn 重启失败 ❌"
        log_error "请查看日志: tail -50 /www/wwwlogs/campus-wall-error.log"
    fi
}

# ========== 日志函数 ==========
show_logs() {
    log_step "显示最近错误日志..."
    echo ""
    tail -30 /www/wwwlogs/campus-wall-error.log
}

# ========== 回滚函数 ==========
rollback() {
    log_step "可用的备份："
    ls -lt "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | head -5
    echo ""
    read -p "输入要回滚的备份文件名（如 backup_20260530_120000.tar.gz）: " BACKUP_FILE

    if [[ -f "$BACKUP_DIR/$BACKUP_FILE" ]]; then
        if confirm "确认回滚到 $BACKUP_FILE？这将覆盖当前代码"; then
            log_step "回滚中..."
            # 备份当前
            backup
            # 解压备份
            tar -xzf "$BACKUP_DIR/$BACKUP_FILE" -C /
            # 重启
            restart
            log_info "回滚完成"
        fi
    else
        log_error "备份文件不存在: $BACKUP_DIR/$BACKUP_FILE"
    fi
}

# ========== 主菜单 ==========
show_menu() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}    校园墙 (Campus Wall) 部署管理${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "  1) 完整部署 (备份+更新+迁移+重启)"
    echo "  2) 仅重启服务"
    echo "  3) 查看服务状态"
    echo "  4) 查看错误日志"
    echo "  5) 回滚到备份"
    echo "  0) 退出"
    echo ""
    read -p "请选择操作 [0-5]: " CHOICE

    case $CHOICE in
        1) deploy ;;
        2) restart ;;
        3) check_status ;;
        4) show_logs ;;
        5) rollback ;;
        0) exit 0 ;;
        *) log_error "无效选择" ;;
    esac
}

# ========== 入口 ==========
case "$1" in
    --force)   deploy --force ;;
    --restart) restart ;;
    --check)   check_status ;;
    --logs)    show_logs ;;
    --rollback) rollback ;;
    *)         show_menu ;;
esac
