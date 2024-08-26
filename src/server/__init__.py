import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.database import init_db
from src.server.auth.router import api as auth_api
from src.server.utils.router import api as utils_api

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


""" 
Server Package Descriptions: 
1. `router.py` - core of each module with all the endpoints 
2. `schemas.py` - pydantic models 
3. `models.py` - db models 
4. `service.py` - module specific business logic 
5. `dependencies.py` - router dependencies 
6. `constants.py` - module specific constants and error codes 
7. `config.py` - env vars 
8. `utils.py` - non-business logic functions 
9. `exceptions.py` - module specific exceptions 

Notes: 
1. FastAPI runs `sync` routes in the `threadpool` and blocking I/O operations won't stop the event loop from executing tasks. 
"""