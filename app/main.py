import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.constant import CHARTS_ROUTE, TABLES_ROUTE
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

    if not get_settings().charts_output_dir.exists():
        get_settings().charts_output_dir.mkdir()

    if not get_settings().table_snippet_output_dir.exists():
        get_settings().table_snippet_output_dir.mkdir()

    app.mount(
        CHARTS_ROUTE,
        StaticFiles(directory=get_settings().charts_output_dir),
        name="charts",
    )
    app.mount(
        TABLES_ROUTE,
        StaticFiles(directory=get_settings().table_snippet_output_dir),
        name="tables",
    )

    return app


app = get_app()
