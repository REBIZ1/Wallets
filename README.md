# Wallets

REST API для управления кошельком.

## Репозиторий

```bash
https://github.com/REBIZ1/Wallets
```

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone git@github.com:REBIZ1/Wallets.git
```

2. Создать файл `.env`:

Пример:
```.env
MODE="LOCAL"

DB_USER=postgres
DB_PASS=postgres
DB_HOST=wallets_db
DB_PORT=5432
DB_NAME=wallets
```

3. Запустить проект:

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```bash
http://localhost:7777
```

Swagger документация:

```bash
http://localhost:7777/docs
```

## Используемые технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose
