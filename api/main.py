from fastapi import FastAPI

from api.routes import router


def create_app():
    app = FastAPI(
        title="FastAPI App",
        description="API para evaluar módulo de programación avanzada",
        version="1.0.0"
    )

    app.include_router(router)

    return app

app = create_app()
