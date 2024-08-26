import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.database import init_db, cleanup
from src.server.auth.endpoint import api as auth_api
from src.server.utils.endpoint import api as utils_api

logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    SessionMiddleware,
    secret_key="secret-key"
)


@app.on_event("startup")
async def startup_event():
    logger.info(f"Server is starting")
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Server is shutting down..")
    await cleanup()

app.include_router(utils_api)
app.include_router(auth_api)
