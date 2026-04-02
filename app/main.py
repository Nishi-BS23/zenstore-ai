from fastapi import FastAPI

from app.api.v1 import api_router
from app.api.v1.health import router as health_router


app = FastAPI(title="Zenstore AI API")

app.include_router(health_router)
app.include_router(api_router, prefix="/api/v1")

