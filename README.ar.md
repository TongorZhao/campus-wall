# Campus Wall - جدار الحرم الجامعي

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | العربية | [Português](README.pt.md)

نظام منتدى مجهول الهوية/عام للحرم الجامعي مبني على Django.

## الميزات

- تسجيل المستخدمين، تسجيل الدخول، إدارة الملفات الشخصية
- النشر (دعم رفع الصور، النشر المجهول)
- التعليقات، الردود، الإعجاب
- حفظ المنشورات
- نظام التصنيفات والوسوم
- البحث النصي الكامل
- نظام الرسائل الخاصة
- نظام الإشعارات
- وظيفة الإبلاغ
- نظام المتابعين
- لوحة التحكم của الإدارة

## التقنيات

- **الخلفية**: Django 4.2 + PostgreSQL
- **الواجهة الأمامية**: Bootstrap 5 + Bootstrap Icons
- **الوقت الحقيقي**: Django Channels + Redis

## التثبيت

### المتطلبات

- Python 3.10+
- PostgreSQL 12+
- Redis (لـ WebSocket)

### الإعداد

```bash
# استنساخ المشروع
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو venv\Scripts\activate  # Windows

# تثبيت التبعيات
pip install -r requirements.txt

# تكوين متغيرات البيئة
cp .env.example .env
# تعديل ملف .env بإعداداتك

# ترحيل قاعدة البيانات
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# إنشاء مستخدم خارق
python manage.py createsuperuser

# تهيئة التصنيفات
python manage.py init_categories

# جمع الملفات الثابتة
python manage.py collectstatic

# تشغيل خادم التطوير
python manage.py runserver
```

### الإنتاج

```bash
# استخدام Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# استخدام Daphne (دعم WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# تكوين Nginx (انظر nginx.conf.example)
```

## هيكل المشروع

```
campus-wall/
├── config/                 # تكوين المشروع
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # التطبيقات
│   ├── accounts/           # إدارة المستخدمين
│   ├── posts/              # إدارة المنشورات
│   ├── messages_app/       # الرسائل الخاصة
│   └── notifications/      # نظام الإشعارات
├── templates/              # ملفات القوالب
├── static/                 # الملفات الثابتة
├── media/                  # رفع المستخدمين
├── manage.py
└── requirements.txt
```

## التصنيفات الافتراضية

- جدار الاعترافات
- المفقودات والمعثورات
- التجارة الثانية
- التعبير عن المشاعر
- تبادل الدراسة
- أنشطة النوادي
- أخبار الحرم الجامعي
- أخرى

## ملاحظات

1. قم بتغيير `DJANGO_SECRET_KEY` في بيئة الإنتاج
2. قم بتعيين `DJANGO_DEBUG=False` في بيئة الإنتاج
3. تأكد من تشغيل خدمات PostgreSQL و Redis
4. نسخ احتياطي لقاعدة البيانات بانتظام
5. تكوين سياسات CORS والأمان المناسبة
