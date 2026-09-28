from fastapi import FastAPI


def create_app():
    app = FastAPI(
        title="FastAPI App",
        description="API para evaluar módulo de programación avanzada",
        version="1.0.0"
    )

    @app.get("/")
    async def home():
        return {"message": "It's working!"}

    return app

app = create_app()
