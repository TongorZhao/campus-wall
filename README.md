# Campus Wall - 校园墙

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

一个基于 Django 的校园匿名/公开论坛系统。

## 功能特性

- 用户注册、登录、个人资料管理
- 发帖（支持图片上传、匿名发布）
- 评论、回复、点赞
- 收藏帖子
- 分类、标签系统
- 全文搜索
- 私信系统
- 通知系统
- 举报功能
- 关注/粉丝系统
- 管理后台

## 技术栈

- **后端**: Django 4.2 + PostgreSQL
- **前端**: Bootstrap 5 + Bootstrap Icons
- **实时通信**: Django Channels + Redis

## 安装部署

### 1. 环境要求

- Python 3.10+
- PostgreSQL 12+
- Redis (用于 WebSocket)

### 2. 安装步骤

```bash
# 克隆项目
git clone <your-repo-url>
cd campus-wall

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的配置

# 数据库迁移
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化分类
python manage.py init_categories

# 收集静态文件
python manage.py collectstatic

# 运行开发服务器
python manage.py runserver
```

### 3. 生产部署

```bash
# 使用 Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# 使用 Daphne (支持 WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# 配置 Nginx (参考 nginx.conf.example)
```

## 项目结构

```
campus-wall/
├── config/                 # 项目配置
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # 应用目录
│   ├── accounts/           # 用户管理
│   ├── posts/              # 帖子管理
│   ├── messages_app/       # 私信功能
│   └── notifications/      # 通知系统
├── templates/              # 模板文件
├── static/                 # 静态文件
├── media/                  # 用户上传文件
├── manage.py
└── requirements.txt
```

## 默认分类

- 表白墙
- 失物招领
- 二手交易
- 吐槽树洞
- 学习交流
- 社团活动
- 校园资讯
- 其他

## 注意事项

1. 生产环境请修改 `DJANGO_SECRET_KEY`
2. 生产环境请设置 `DJANGO_DEBUG=False`
3. 确保 PostgreSQL 和 Redis 服务正常运行
4. 定期备份数据库
5. 配置合适的 CORS 和安全策略
