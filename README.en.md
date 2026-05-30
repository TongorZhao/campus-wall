# Campus Wall

[中文](README.md) | [English](README.en.md)

A campus anonymous/public forum system based on Django.

## Features

- User registration, login, profile management
- Posting (support image upload, anonymous posting)
- Comments, replies, likes
- Bookmark posts
- Category and tag system
- Full-text search
- Private messaging
- Notification system
- Report function
- Follow/follower system
- Admin dashboard

## Tech Stack

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Real-time**: Django Channels + Redis

## Installation

### Requirements

- Python 3.10+
- PostgreSQL 12+
- Redis (for WebSocket)

### Setup

```bash
# Clone project
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your settings

# Database migration
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Initialize categories
python manage.py init_categories

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

### Production

```bash
# Use Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Use Daphne (WebSocket support)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Configure Nginx (see nginx.conf.example)
```

## Project Structure

```
campus-wall/
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Applications
│   ├── accounts/           # User management
│   ├── posts/              # Post management
│   ├── messages_app/       # Private messaging
│   └── notifications/      # Notification system
├── templates/              # Template files
├── static/                 # Static files
├── media/                  # User uploads
├── manage.py
└── requirements.txt
```

## Default Categories

- Confession Wall
- Lost & Found
- Second-hand Trading
- Vent & Thoughts
- Study Exchange
- Club Activities
- Campus News
- Others

## Notes

1. Change `DJANGO_SECRET_KEY` in production
2. Set `DJANGO_DEBUG=False` in production
3. Ensure PostgreSQL and Redis services are running
4. Backup database regularly
5. Configure appropriate CORS and security policies
