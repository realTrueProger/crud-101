Python FastAPI CRUD

## Requirements
- Python 3.12
- FastAPI
- PostgreSQL 

## Запуск
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
docker compose up -d // запуск postgress
fastapi dev app/main.py // запуск api
```


## Переменные окружения

Создай файл `.env` в корне проекта и заполни переменные:

### PostgreSQL (Docker Compose)
- **POSTGRES_USER** — имя пользователя базы данных (например, `rootuser`).
- **POSTGRES_PASSWORD** — пароль пользователя (например, `secret`).
- **POSTGRES_DB** — имя базы данных (например, `appdb`).
- **POSTGRES_PORT** — порт PostgreSQL внутри контейнера (обычно `5432`).

### Приложение (FastAPI + SQLAlchemy)
- **DATABASE_URL** — строка подключения к базе.  
  Формат: 
```
postgresql+psycopg://<user>:<password>@<host>:<port>/<dbname>