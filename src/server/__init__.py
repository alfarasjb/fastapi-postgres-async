import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.database import init_db
from src.server.auth.endpoint import api as auth_api
from src.server.utils.endpoint import api as utils_api

logger = logging.getLogger(__name__)

# This can also be used. This will be the `lifespan` parameter in the FastAPI instance.
# Use lifespan because on_event is deprecated


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing Database")
    await init_db()
    yield
    logger.info(f"Database is shutting down.")


app = FastAPI(
    title="Async FastAPI + Postgres",
    description="A simple server using Async FastAPI and Postgres",
    lifespan=lifespan
)

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


app.include_router(utils_api)
app.include_router(auth_api)
