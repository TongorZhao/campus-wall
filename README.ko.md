# Campus Wall - 캠퍼스 월

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | 한국어 | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

Django 기반 캠퍼스 익명/공개 포럼 시스템.

## 기능

- 사용자 등록, 로그인, 프로필 관리
- 게시물 작성 (이미지 업로드, 익명 게시 지원)
- 댓글, 답글, 좋아요
- 게시물 북마크
- 카테고리 및 태그 시스템
- 전문 검색
- 쪽지 시스템
- 알림 시스템
- 신고 기능
- 팔로우/팔로워 시스템
- 관리자 대시보드

## 기술 스택

- **백엔드**: Django 4.2 + PostgreSQL
- **프론트엔드**: Bootstrap 5 + Bootstrap Icons
- **실시간**: Django Channels + Redis

## 설치

### 요구사항

- Python 3.10+
- PostgreSQL 12+
- Redis (WebSocket용)

### 설정

```bash
# 프로젝트 클론
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 설정 입력

# 데이터베이스 마이그레이션
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 카테고리 초기화
python manage.py init_categories

# 정적 파일 수집
python manage.py collectstatic

# 개발 서버 실행
python manage.py runserver
```

### 프로덕션

```bash
# Gunicorn 사용
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Daphne 사용 (WebSocket 지원)
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Nginx 설정 (nginx.conf.example 참조)
```

## 프로젝트 구조

```
campus-wall/
├── config/                 # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # 애플리케이션
│   ├── accounts/           # 사용자 관리
│   ├── posts/              # 게시물 관리
│   ├── messages_app/       # 쪽지 기능
│   └── notifications/      # 알림 시스템
├── templates/              # 템플릿 파일
├── static/                 # 정적 파일
├── media/                  # 사용자 업로드
├── manage.py
└── requirements.txt
```

## 기본 카테고리

- 고백의 벽
- 분실물/습득물
- 중고 거래
- 불만 토로
- 학습 교류
- 동아리 활동
- 캠퍼스 뉴스
- 기타

## 주의사항

1. 프로덕션 환경에서 `DJANGO_SECRET_KEY`를 변경하세요
2. 프로덕션 환경에서 `DJANGO_DEBUG=False`를 설정하세요
3. PostgreSQL과 Redis 서비스가 실행 중인지 확인하세요
4. 정기적으로 데이터베이스를 백업하세요
5. 적절한 CORS 및 보안 정책을 구성하세요
