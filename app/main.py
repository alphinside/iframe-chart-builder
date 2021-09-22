import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import api_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s : %(levelname)s : %(message)s"
)


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(api_router, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_app()
