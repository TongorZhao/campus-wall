# Campus Wall - Campuswand

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | Deutsch | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

Ein anonymes/öffentliches Campus-Forum-System basierend auf Django.

## Funktionen

- Benutzerregistrierung, Anmeldung, Profilverwaltung
- Beiträge erstellen (Bilder hochladen, anonyme Beiträge)
- Kommentare, Antworten, Likes
- Beiträge speichern
- Kategorien- und Tag-System
- Volltextsuche
- Privates Nachrichtensystem
- Benachrichtigungssystem
- Meldungsfunktion
- Follower/Following-System
- Admin-Dashboard

## Tech-Stack

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Echtzeit**: Django Channels + Redis

## Installation

### Voraussetzungen

- Python 3.10+
- PostgreSQL 12+
- Redis (für WebSocket)

### Einrichtung

```bash
# Projekt klonen
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
cp .env.example .env
# .env-Datei mit deinen Einstellungen bearbeiten

# Datenbank-Migration
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Superuser erstellen
python manage.py createsuperuser

# Kategorien initialisieren
python manage.py init_categories

# Statische Dateien sammeln
python manage.py collectstatic

# Entwicklungsserver starten
python manage.py runserver
```

### Produktion

```bash
# Gunicorn verwenden
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Daphne verwenden (WebSocket-Unterstützung)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Nginx konfigurieren (siehe nginx.conf.example)
```

## Projektstruktur

```
campus-wall/
├── config/                 # Projektkonfiguration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Anwendungen
│   ├── accounts/           # Benutzerverwaltung
│   ├── posts/              # Beitragsverwaltung
│   ├── messages_app/       # Private Nachrichten
│   └── notifications/      # Benachrichtigungssystem
├── templates/              # Vorlagendateien
├── static/                 # Statische Dateien
├── media/                  # Benutzer-Uploads
├── manage.py
└── requirements.txt
```

## Standardkategorien

- Liebeswand
- Fundsachen
- Gebrauchtkauf
- Dampf ablassen
- Lern Austausch
- Vereinsaktivitäten
- Campus Nachrichten
- Sonstiges

## Hinweise

1. Ändere `DJANGO_SECRET_KEY` in der Produktion
2. Setze `DJANGO_DEBUG=False` in der Produktion
3. Stelle sicher, dass PostgreSQL und Redis laufen
4. Sichere die Datenbank regelmäßig
5. Konfiguriere geeignete CORS- und Sicherheitsrichtlinien
