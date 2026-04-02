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

## Health Check

```bash
curl http://127.0.0.1:9072/health
```
