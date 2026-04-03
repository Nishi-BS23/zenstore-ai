# Zenstore AI

Minimal FastAPI scaffold.

## Requirements

- Python 3.10+
- `pip`

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is empty, install baseline packages:

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
```

## Run

Start the API on port `9072`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9072 --reload
```

## Celery Worker

Run the background worker with Redis as broker/backend:

```bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

## Redis

Set `REDIS_URL` in `.env` if Redis is not on the default local port:

```env
REDIS_URL=redis://localhost:6379/0
```

## Health Check

```bash
curl http://127.0.0.1:9072/health
```

## Migrations

Migration naming convention:

- `YYYYMMDD_0001_description`
- Example: `20250819_0001_add_user_account_deactivations`

Create a new migration using the helper script:

```bash
./scripts/new_migration.sh "add user account deactivations"
```

Apply migrations:

```bash
/home/bs00956/Desktop/Personal/zenstore-ai/venv/bin/python -m alembic upgrade head
```
