import uvicorn
from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.container import Container


def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()
    app.container = container
    app.include_router(v1_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
