from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config.database import create_tables
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

def create_app():
    app = FastAPI(
        title="FastAPI App",
        description="API para evaluar módulo de programación avanzada",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(router)

    return app

app = create_app()
