# Zenstore AI

Zenstore AI is a production-grade FastAPI backend for authenticated product management, asynchronous AI enrichment, CSV bulk ingestion, and Redis-backed caching.

It follows a clean, layered architecture designed for maintainability, testability, and operational clarity.

## Highlights

- JWT-based authentication with bcrypt password hashing
- Owner-scoped product CRUD APIs
- Asynchronous AI enrichment via Celery
- CSV bulk upload with streaming row processing
- Cache-aside Redis strategy for product reads
- Repository layer for consistent and testable persistence
- Pytest suite with isolated SQLite test database

## Technology Stack

- FastAPI
- SQLAlchemy + Alembic
- Celery + Redis
- PyJWT + bcrypt
- Pytest + TestClient

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9072 --reload
```

Health check:

```bash
curl http://127.0.0.1:9072/health
```

## Configuration

The application reads environment variables from `.env`.

```env
DATABASE_URL=sqlite:///./zenstore.db
SECRET_KEY=replace-with-a-long-random-secret
REDIS_URL=redis://localhost:6379/0

AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your-groq-key
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Configuration Reference

| Variable | Purpose | Example |
| --- | --- | --- |
| `DATABASE_URL` | Database connection string | `sqlite:///./zenstore.db` |
| `SECRET_KEY` | JWT signing secret | `replace-with-a-long-random-secret` |
| `REDIS_URL` | Redis URL for cache and Celery | `redis://localhost:6379/0` |
| `AI_PROVIDER` | AI provider selector | `groq` or `openai` |
| `AI_MODEL` | Model identifier | `llama-3.1-8b-instant` |
| `GROQ_API_KEY` | Groq API key | `your-groq-key` |
| `OPENAI_API_KEY` | OpenAI API key | `your-openai-key` |
| `OPENAI_BASE_URL` | OpenAI API base URL | `https://api.openai.com/v1` |

## Architecture

```text
Route -> Service -> Repository -> Model -> Database
```

### Layers

- **API Layer** (`app/api/`): request validation, HTTP responses, dependency injection
- **Service Layer** (`app/services/`): business logic and orchestration
- **Repository Layer** (`app/repositories/`): SQLAlchemy persistence and queries
- **Model Layer** (`app/models/`): ORM models and relationships
- **Worker Layer** (`app/workers/`): background tasks and async processing

This separation keeps the codebase modular and test-friendly.

## Runtime Flows

### Authentication

1. `POST /api/v1/auth/register` creates the user
2. `POST /api/v1/auth/login` issues a JWT
3. Protected endpoints require `Authorization: Bearer <token>`

### Product Create

1. `POST /api/v1/products` accepts product payload
2. `get_current_user()` validates JWT
3. `ProductRepository.create()` inserts the product
4. `generate_ai_content.delay(product.id)` queues AI job
5. API returns `202 Accepted`

### Product Read

1. `GET /api/v1/products/{id}` checks Redis cache
2. On cache miss, DB is queried via repository
3. Response is serialized and optionally cached

### Bulk Upload

1. `POST /api/v1/products/bulk` validates CSV file
2. Rows are streamed and inserted
3. AI jobs are queued per row
4. API returns `202 Accepted` with `job_id`

## API Surface

Base path: `/api/v1`

### Auth

- `POST /auth/register` → `201 Created`
- `POST /auth/login` → `200 OK`
- `GET /auth/me` → `200 OK`

### Products

- `POST /products` → `202 Accepted`
- `GET /products` → `200 OK`
- `GET /products/{product_id}` → `200 OK`
- `PUT /products/{product_id}` → `200 OK`
- `DELETE /products/{product_id}` → `204 No Content`
- `POST /products/bulk` → `202 Accepted`

### Common Errors

- `400 Bad Request` for invalid input or file type
- `401 Unauthorized` for missing/invalid token
- `404 Not Found` for missing resources

## Project Structure

```text
app/
	api/            # routes and dependencies
	core/           # config, database, security
	models/         # SQLAlchemy models
	repositories/   # data access layer
	schemas/        # request/response contracts
	services/       # business logic
	utils/          # helpers, decorators
	workers/        # Celery config and tasks
tests/            # pytest test suite
docs/             # detailed design notes
```

## Docker

This project includes Docker support for running API, worker, Redis, and Postgres together.

### Files

- `Dockerfile`
- `docker-compose.yml`
- `.env.docker`

### Ports (Host -> Container)

- API: `9071 -> 9071`
- Redis: `6380 -> 6379`
- Postgres: `5434 -> 5432`

### Build and Run

```bash
docker compose up -d --build
```

Apply migrations inside the API container:

```bash
docker compose exec api python -m alembic upgrade head
```

Health check:

```bash
curl http://127.0.0.1:9071/health
```

### Docker Environment

`docker-compose.yml` uses `.env.docker` for container settings. Example:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/zenstore
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-prod-secret-key-32chars
AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your-key-here
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Common Docker Commands

```bash
docker compose up -d
docker compose down
docker compose logs -f api
docker compose down -v
```

## Migrations

Create a migration:

```bash
./scripts/new_migration.sh "add user account deactivations"
```

Apply migrations:

```bash
./venv/bin/python -m alembic upgrade head
```

Rollback:

```bash
./venv/bin/python -m alembic downgrade -1
```

## Testing

Run the full test suite:

```bash
./venv/bin/pytest -q
```

### Testing Design

- `tests/conftest.py` provides shared fixtures
- `client` uses FastAPI `TestClient`
- `db_session` uses isolated SQLite (`test.db`)
- schema is recreated per test for deterministic results
- `auth_headers` generates valid JWT headers for protected endpoints

### Core Test Coverage

- auth register/login
- invalid login handling
- product create/read/auth guard
- bulk CSV upload and invalid file type

## Operations

### Run API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9072 --reload
```

### Run Celery Worker

```bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

### Health and Docs

- Health: `http://127.0.0.1:9072/health`
- Docs: `http://127.0.0.1:9072/docs`
- ReDoc: `http://127.0.0.1:9072/redoc`

## Operational Guidance

- Use a strong `SECRET_KEY` in non-local environments
- Ensure Redis is running before using caching or Celery
- Product creation is intentionally asynchronous (`202 Accepted`)

## Troubleshooting

### JWT key length warnings

Use a longer `SECRET_KEY` (32+ characters).

### Celery tasks not running

- Ensure Redis is up
- Start the worker process
- Verify `REDIS_URL` is correct

### Test DB issues

Delete `test.db` if you suspect stale state and rerun tests.


## License

Internal project.
