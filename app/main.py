import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware

from app.config import get_settings
from app.constant import DASH_MOUNT_ROUTE
from app.dash_app import dash_app
from app.data_manager import create_dir_dependencies, populate_persisted_data
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

    app.mount(DASH_MOUNT_ROUTE, WSGIMiddleware(dash_app.server))

    create_dir_dependencies()
    populate_persisted_data()

    # app.mount(
    #     CHARTS_ROUTE,
    #     StaticFiles(directory=get_settings().charts_output_dir),
    #     name="charts",
    # )
    # app.mount(
    #     TABLES_ROUTE,
    #     StaticFiles(directory=get_settings().table_snippet_output_dir),
    #     name="tables",
    # )

    return app


app = get_app()
