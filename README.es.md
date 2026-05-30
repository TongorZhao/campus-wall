# Campus Wall - Muro del Campus

[中文](README.md) | [English](README.en.md) | Español | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

Un sistema de foro anónimo/público del campus basado en Django.

## Características

- Registro de usuarios, inicio de sesión, gestión de perfiles
- Publicación de mensajes (soporte para carga de imágenes, publicación anónima)
- Comentarios, respuestas, me gusta
- Guardar publicaciones
- Sistema de categorías y etiquetas
- Búsqueda de texto completo
- Sistema de mensajería privada
- Sistema de notificaciones
- Función de reporte
- Sistema de seguidores/seguidos
- Panel de administración

## Stack Tecnológico

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Tiempo real**: Django Channels + Redis

## Instalación

### Requisitos

- Python 3.10+
- PostgreSQL 12+
- Redis (para WebSocket)

### Configuración

```bash
# Clonar proyecto
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar archivo .env con tu configuración

# Migración de base de datos
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Inicializar categorías
python manage.py init_categories

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar servidor de desarrollo
python manage.py runserver
```

### Producción

```bash
# Usar Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Usar Daphne (soporte WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Configurar Nginx (ver nginx.conf.example)
```

## Estructura del Proyecto

```
campus-wall/
├── config/                 # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Aplicaciones
│   ├── accounts/           # Gestión de usuarios
│   ├── posts/              # Gestión de publicaciones
│   ├── messages_app/       # Mensajería privada
│   └── notifications/      # Sistema de notificaciones
├── templates/              # Archivos de plantilla
├── static/                 # Archivos estáticos
├── media/                  # Subidas de usuarios
├── manage.py
└── requirements.txt
```

## Categorías Predeterminadas

- Muro de Confesiones
- Perdidos y Encontrados
- Segunda Mano
- Desahogo y Pensamientos
- Intercambio de Estudios
- Actividades de Clubes
- Noticias del Campus
- Otros

## Notas

1. Cambia `DJANGO_SECRET_KEY` en producción
2. Configura `DJANGO_DEBUG=False` en producción
3. Asegúrate de que PostgreSQL y Redis estén funcionando
4. Realiza copias de seguridad de la base de datos regularmente
5. Configura políticas de CORS y seguridad apropiadas
