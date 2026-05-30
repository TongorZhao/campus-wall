# Campus Wall - Mur du Campus

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | Français | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

Un système de forum anonyme/public du campus basé sur Django.

## Fonctionnalités

- Inscription des utilisateurs, connexion, gestion des profils
- Publication (support de téléchargement d'images, publication anonyme)
- Commentaires, réponses, mentions j'aime
- Sauvegarder les publications
- Système de catégories et de tags
- Recherche en texte intégral
- Système de messagerie privée
- Système de notifications
- Fonction de signalement
- Système d'abonnés/abonnements
- Panneau d'administration

## Stack Technique

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Temps réel**: Django Channels + Redis

## Installation

### Prérequis

- Python 3.10+
- PostgreSQL 12+
- Redis (pour WebSocket)

### Configuration

```bash
# Cloner le projet
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer le fichier .env avec votre configuration

# Migration de la base de données
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Créer le superutilisateur
python manage.py createsuperuser

# Initialiser les catégories
python manage.py init_categories

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer le serveur de développement
python manage.py runserver
```

### Production

```bash
# Utiliser Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Utiliser Daphne (support WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Configurer Nginx (voir nginx.conf.example)
```

## Structure du Projet

```
campus-wall/
├── config/                 # Configuration du projet
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Applications
│   ├── accounts/           # Gestion des utilisateurs
│   ├── posts/              # Gestion des publications
│   ├── messages_app/       # Messagerie privée
│   └── notifications/      # Système de notifications
├── templates/              # Fichiers de modèle
├── static/                 # Fichiers statiques
├── media/                  # Téléchargements utilisateur
├── manage.py
└── requirements.txt
```

## Catégories par Défaut

- Mur des Confessions
- Objets Trouvés/Perdus
- Vente entre Particuliers
- Confidences et Réflexions
- Échange d'Études
- Activités des Clubs
- Actualités du Campus
- Autres

## Notes

1. Modifiez `DJANGO_SECRET_KEY` en production
2. Définissez `DJANGO_DEBUG=False` en production
3. Assurez-vous que PostgreSQL et Redis sont en cours d'exécution
4. Sauvegardez régulièrement la base de données
5. Configurez les politiques CORS et de sécurité appropriées
