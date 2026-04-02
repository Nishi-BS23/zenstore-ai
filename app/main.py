from fastapi import FastAPI

from app.api.v1 import api_router
from app.api.v1.health import router as health_router


def create_app() -> FastAPI:
	app = FastAPI(title="Zenstore AI API")
	app.include_router(health_router)
	app.include_router(api_router, prefix="/api/v1")
	return app


app = create_app()


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

