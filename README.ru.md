# Campus Wall - Стена Кампуса

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | Русский | [العربية](README.ar.md) | [Português](README.pt.md)

Анонимная/публичная система форумов кампуса на основе Django.

## Возможности

- Регистрация пользователей, вход, управление профилями
- Публикация постов (загрузка изображений, анонимная публикация)
- Комментарии, ответы, лайки
- Сохранение постов
- Система категорий и тегов
- Полнотекстовый поиск
- Система личных сообщений
- Система уведомлений
- Функция жалоб
- Система подписчиков/подписок
- Админ-панель

## Технологический Стек

- **Бэкенд**: Django 4.2 + PostgreSQL
- **Фронтенд**: Bootstrap 5 + Bootstrap Icons
- **Реальное время**: Django Channels + Redis

## Установка

### Требования

- Python 3.10+
- PostgreSQL 12+
- Redis (для WebSocket)

### Настройка

```bash
# Клонировать проект
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать файл .env с вашими настройками

# Миграция базы данных
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Инициализировать категории
python manage.py init_categories

# Собрать статические файлы
python manage.py collectstatic

# Запустить сервер разработки
python manage.py runserver
```

### Продакшн

```bash
# Использовать Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Использовать Daphne (поддержка WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Настроить Nginx (см. nginx.conf.example)
```

## Структура Проекта

```
campus-wall/
├── config/                 # Конфигурация проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Приложения
│   ├── accounts/           # Управление пользователями
│   ├── posts/              # Управление постами
│   ├── messages_app/       # Личные сообщения
│   └── notifications/      # Система уведомлений
├── templates/              # Файлы шаблонов
├── static/                 # Статические файлы
├── media/                  # Загрузки пользователей
├── manage.py
└── requirements.txt
```

## Категории по Умолчанию

- Стена признаний
- Потерянные и найденные вещи
- Барахолка
- Выплеснуть эмоции
- Обмен учебным опытом
- Деятельность клубов
- Новости кампуса
- Прочее

## Примечания

1. Измените `DJANGO_SECRET_KEY` в продакшне
2. Установите `DJANGO_DEBUG=False` в продакшне
3. Убедитесь, что PostgreSQL и Redis работают
4. Регулярно создавайте резервные копии базы данных
5. Настройте соответствующие политики CORS и безопасности
