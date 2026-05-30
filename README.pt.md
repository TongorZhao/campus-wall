# Campus Wall - Muro do Campus

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | Português

Um sistema de fórum anônimo/público do campus baseado em Django.

## Funcionalidades

- Registro de usuários, login, gerenciamento de perfil
- Publicação (suporte a upload de imagens, publicação anônima)
- Comentários, respostas, curtidas
- Salvar publicações
- Sistema de categorias e tags
- Busca em texto completo
- Sistema de mensagens privadas
- Sistema de notificações
- Função de denúncia
- Sistema de seguidores/seguidos
- Painel de administração

## Stack Técnico

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Tempo real**: Django Channels + Redis

## Instalação

### Requisitos

- Python 3.10+
- PostgreSQL 12+
- Redis (para WebSocket)

### Configuração

```bash
# Clonar projeto
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar arquivo .env com suas configurações

# Migração do banco de dados
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Inicializar categorias
python manage.py init_categories

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Produção

```bash
# Usar Gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Usar Daphne (suporte WebSocket)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Configurar Nginx (ver nginx.conf.example)
```

## Estrutura do Projeto

```
campus-wall/
├── config/                 # Configuração do projeto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Aplicações
│   ├── accounts/           # Gerenciamento de usuários
│   ├── posts/              # Gerenciamento de publicações
│   ├── messages_app/       # Mensagens privadas
│   └── notifications/      # Sistema de notificações
├── templates/              # Arquivos de modelo
├── static/                 # Arquivos estáticos
├── media/                  # Uploads de usuários
├── manage.py
└── requirements.txt
```

## Categorias Padrão

- Muro de Confissões
- Achados e Perdidos
- Segunda Mão
- Desabafo e Reflexões
- Intercâmbio de Estudos
- Atividades de Clubes
- Notícias do Campus
- Outros

## Notas

1. Altere `DJANGO_SECRET_KEY` em produção
2. Defina `DJANGO_DEBUG=False` em produção
3. Certifique-se de que PostgreSQL e Redis estejam em execução
4. Faça backup do banco de dados regularmente
5. Configure políticas CORS e de segurança apropriadas
