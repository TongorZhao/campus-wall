# Campus Wall (校园墙) - AI 助手开发指南

## 项目概述

校园墙是一个基于 Django 的校园社区论坛，支持帖子发布（含图片）、评论、点赞、收藏、私信、通知、关注等功能。

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Django 4.2 |
| 数据库 | PostgreSQL |
| 缓存/消息 | Redis |
| 实时通信 | Django Channels (WebSocket) |
| 前端 | Bootstrap 5.3 + Bootstrap Icons |
| 静态文件 | WhiteNoise |
| 生产服务器 | Gunicorn (WSGI) + Nginx |
| 部署环境 | 宝塔面板 |

### 服务器信息

```
项目路径: /www/wwwroot/campus-wall
Python: 3.12 (venv)
数据库: campus_wall (PostgreSQL)
```

---

## 目录结构

```
campus-wall/
├── apps/
│   ├── accounts/          # 用户管理（注册、登录、资料、关注）
│   ├── posts/             # 帖子管理（CRUD、分类、标签、点赞、评论、收藏）
│   ├── messages_app/      # 私信系统
│   └── notifications/     # 通知和举报
├── config/
│   ├── settings.py        # Django 配置
│   ├── urls.py            # 根路由
│   ├── asgi.py            # ASGI 配置 (WebSocket)
│   └── wsgi.py            # WSGI 配置
├── templates/             # HTML 模板
│   ├── base/              # 基础模板
│   ├── posts/             # 帖子相关模板
│   ├── accounts/          # 用户相关模板
│   ├── messages/          # 私信模板
│   ├── notifications/     # 通知模板
│   └── components/        # 可复用组件（如评论）
├── static/                # 静态文件
│   ├── css/style.css
│   └── js/main.js
├── media/                 # 用户上传文件（头像、帖子图片）
├── .env                   # 环境变量（敏感，不入 git）
├── .env.example           # 环境变量模板
├── .gitignore             # Git 忽略规则
├── requirements.txt       # Python 依赖
├── manage.py              # Django 管理脚本
├── deploy.sh              # 部署脚本
└── nginx.conf.example     # Nginx 配置示例
```

---

## 核心模型

### 用户模型 (accounts.User)

```python
# 继承 AbstractUser，扩展以下字段
- nickname      # 昵称
- avatar        # 头像 (ImageField)
- bio           # 个人简介
- school        # 学校
- grade         # 年级
- phone         # 手机号
- is_verified   # 是否认证
```

### 帖子模型 (posts.Post)

```python
- title         # 标题
- content       # 内容
- author        # 作者 (FK -> User)
- category      # 分类 (FK -> Category)
- tags          # 标签 (M2M -> Tag)
- anonymity     # 匿名状态: 'public' / 'anonymous'
- is_pinned     # 置顶
- is_deleted    # 软删除
- view_count    # 浏览数
- like_count    # 点赞数 (反规范化)
- comment_count # 评论数 (反规范化)
```

### 评论模型 (posts.Comment)

```python
- post          # 所属帖子 (FK -> Post)
- author        # 作者 (FK -> User)
- parent        # 父评论 (FK -> self, 用于嵌套回复)
- content       # 内容
- anonymity     # 匿名状态
- is_deleted    # 软删除
```

### 其他模型

- **Category** - 帖子分类 (slug, icon, order)
- **Tag** - 标签 (name, slug，支持中文)
- **PostImage** - 帖子图片 (每帖最多9张)
- **Like** - 点赞记录
- **CommentLike** - 评论点赞
- **Favorite** - 收藏
- **FollowRelationship** - 关注关系
- **Conversation** - 私信对话
- **Message** - 私信消息
- **Notification** - 通知
- **Report** - 举报

---

## URL 路由

### 帖子 (apps/posts/urls.py)

```
/                       # 首页信息流
/hot/                   # 热门帖子
/category/<slug>/       # 分类帖子
/tag/<slug>/            # 标签帖子 (支持中文 slug)
/search/                # 搜索
/create/                # 发帖
/<int:pk>/              # 帖子详情
/<int:pk>/edit/         # 编辑帖子
/<int:pk>/delete/       # 删除帖子 (软删除)
/<int:pk>/like/         # 点赞切换
/<int:pk>/favorite/     # 收藏切换
/comment/<int:pk>/delete/ # 删除评论
/my/favorites/          # 我的收藏
/my/posts/              # 我的帖子
```

### 用户 (apps/accounts/urls.py)

```
/register/              # 注册
/login/                 # 登录
/logout/                # 退出
/profile/               # 个人中心
/profile/edit/          # 编辑资料
/profile/<username>/    # 他人主页
/follow/<username>/     # 关注/取关
/followers/             # 粉丝列表
/following/             # 关注列表
```

### 私信 (apps/messages_app/urls.py)

```
/messages/              # 对话列表
/messages/new/<username>/ # 发起私信
/messages/<int:pk>/     # 对话详情
/messages/<int:pk>/send/ # 发送消息
```

### 通知 (apps/notifications/urls.py)

```
/notifications/              # 通知列表
/notifications/mark/<int:pk>/ # 标记已读
/notifications/read-all/     # 全部已读
/notifications/delete/<int:pk>/ # 删除通知
/notifications/report/       # 举报
/notifications/api/count/    # 未读数量 API
```

---

## 已知问题与解决方案

### 1. Tag slug 中文支持

**问题**: Django 的 `<slug:slug>` 不支持中文字符

**解决**: 使用 `re_path` 替代 `path`

```python
# 错误
path('tag/<slug:slug>/', views.tag_view, name='tag')

# 正确
re_path(r'^tag/(?P<slug>[-\w]+)/$', views.tag_view, name='tag')
```

### 2. 匿名帖子作者泄露

**问题**: 匿名帖子的模板中 `<a href>` 仍然链接到作者 profile

**解决**: 条件渲染 profile 链接

```html
{% if post.anonymity == 'anonymous' %}
<span class="fw-bold">{{ post.get_author_display }}</span>
{% else %}
<a href="{% url 'accounts:user_profile' username=post.author.username %}">
    {{ post.get_author_display }}
</a>
{% endif %}
```

### 3. 私信列表 get_other_participant

**问题**: Django 模板不能调用带参数的方法

**解决**: 在视图中预计算并缓存到对象属性

```python
# views.py
for conv in conversations:
    conv.other_user = conv.participants.exclude(pk=request.user.pk).first()

# template
{% with other=conversation.other_user %}
```

### 4. Django 模板变量命名

**问题**: Django 模板禁止以下划线开头的变量名

**解决**: 不要使用 `_` 开头的属性名

```python
# 错误
conv._cached_other_user = ...

# 正确
conv.other_user = ...
```

### 5. Admin 样式丢失

**问题**: 生产环境 Django admin 无 CSS

**解决**: 运行 `collectstatic`

```bash
python manage.py collectstatic --noinput
```

### 6. 图片上传不显示

**问题 1**: `management_form` 必须在 formset 字段之前

```html
<!-- 正确 -->
{{ formset.management_form }}
{% for form in formset %}
    {{ form.image }}
{% endfor %}

<!-- 错误 -->
{% for form in formset %}
    {{ form.image }}
{% endfor %}
{{ formset.management_form }}
```

**问题 2**: Nginx 未配置 media 文件服务

```nginx
location /media/ {
    alias /www/wwwroot/campus-wall/media/;
    expires 7d;
}
```

### 7. LOGIN_REDIRECT_URL 配置

**问题**: Django 的 `LOGIN_REDIRECT_URL` 期望 URL 路径，不是 URL name

```python
# 错误
LOGIN_REDIRECT_URL = 'posts:feed'

# 正确
LOGIN_REDIRECT_URL = '/'
```

### 8. F() 表达式使用

**问题**: 使用 `F()` 后需要刷新对象

```python
# 错误
Post.objects.filter(pk=pk).update(like_count=F('like_count') + 1)
return JsonResponse({'like_count': post.like_count})  # 旧值

# 正确
Post.objects.filter(pk=pk).update(like_count=F('like_count') + 1)
post.refresh_from_db()
return JsonResponse({'like_count': post.like_count})  # 新值
```

---

## 部署流程

### 标准部署步骤

```bash
# 1. 备份
tar -czf /www/backup/campus-wall-$(date +%Y%m%d).tar.gz \
    --exclude='venv' --exclude='media' --exclude='staticfiles' \
    --exclude='.env' --exclude='__pycache__' \
    /www/wwwroot/campus-wall

# 2. 更新代码（只覆盖代码文件，不动 .env、media、venv）

# 3. 安装依赖
cd /www/wwwroot/campus-wall
./venv/bin/pip install -r requirements.txt

# 4. 数据库迁移
./venv/bin/python manage.py migrate

# 5. 收集静态文件
./venv/bin/python manage.py collectstatic --noinput

# 6. 重启 Gunicorn
pkill -f "gunicorn.*config.wsgi"
nohup ./venv/bin/gunicorn config.wsgi:application \
    -b 0.0.0.0:8000 -w 4 --timeout 120 \
    --access-logfile /www/wwwlogs/campus-wall-access.log \
    --error-logfile /www/wwwlogs/campus-wall-error.log \
    &
```

### 使用部署脚本

```bash
bash deploy.sh           # 交互式菜单
bash deploy.sh --force   # 一键部署
bash deploy.sh --restart # 仅重启
bash deploy.sh --check   # 检查状态
```

### 禁止覆盖的文件

| 文件/目录 | 原因 |
|-----------|------|
| `.env` | 包含数据库密码、SECRET_KEY |
| `media/` | 用户上传的头像和图片 |
| `venv/` | Python 虚拟环境 |
| `staticfiles/` | collectstatic 生成的文件 |
| `*.pyc` | 编译缓存 |

---

## 环境变量 (.env)

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

DB_NAME=campus_wall
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

## 常用管理命令

```bash
# 初始化分类
python manage.py init_categories

# 创建超级用户
python manage.py createsuperuser

# Django shell
python manage.py shell

# 数据库备份
pg_dump -U postgres campus_wall > backup.sql

# 数据库恢复
psql -U postgres campus_wall < backup.sql
```

---

## 代码规范

### Python

- 遵循 PEP 8
- 使用 Django 惯用写法
- 视图函数使用 `@login_required` 装饰器保护需登录页面
- 使用 `select_related` 和 `prefetch_related` 优化查询

### 模板

- 继承 `base/base.html`
- 使用 Bootstrap 5 类名
- 表单使用 `{% csrf_token %}`
- 静态文件使用 `{% static 'path' %}`

### URL

- 使用 `reverse()` 和 `{% url %}` 生成 URL
- 不要硬编码 URL

---

## 修改文件清单

修改代码后需要同步到服务器的文件：

| 目录/文件 | 说明 |
|-----------|------|
| `apps/*/views.py` | 视图逻辑 |
| `apps/*/models.py` | 数据模型 |
| `apps/*/forms.py` | 表单定义 |
| `apps/*/urls.py` | URL 路由 |
| `apps/*/admin.py` | 后台管理 |
| `apps/*/context_processors.py` | 上下文处理器 |
| `templates/**/*.html` | 模板文件 |
| `static/css/style.css` | 自定义样式 |
| `static/js/main.js` | 自定义脚本 |
| `config/settings.py` | 项目配置 |
| `config/urls.py` | 根路由 |
| `requirements.txt` | 依赖列表 |
| `deploy.sh` | 部署脚本 |

**不要同步的文件：**

| 文件 | 原因 |
|------|------|
| `.env` | 敏感配置 |
| `media/` | 用户数据 |
| `venv/` | 虚拟环境 |
| `staticfiles/` | 需在服务器重新生成 |
| `__pycache__/` | 编译缓存 |
| `*.pyc` | 编译缓存 |

---

## 调试技巧

### 查看错误日志

```bash
# Gunicorn 错误日志
tail -50 /www/wwwlogs/campus-wall-error.log

# Nginx 错误日志
tail -50 /www/wwwlogs/<your-domain>.error.log

# Django 系统检查
python manage.py check

# 检查数据库迁移状态
python manage.py showmigrations
```

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 502 Bad Gateway | Gunicorn 崩溃 | 查看错误日志，重启 Gunicorn |
| 403 Forbidden | CSRF 验证失败 | 检查 CSRF token |
| 404 Not Found | URL 配置错误 | 检查 urls.py |
| TemplateSyntaxError | 模板语法错误 | 检查模板文件 |
| NoReverseMatch | URL 反向解析失败 | 检查 URL 名称和参数 |
| OperationalError | 数据库错误 | 检查 .env 数据库配置 |
| ImportError | 模块导入错误 | 检查 INSTALLED_APPS 和导入路径 |
