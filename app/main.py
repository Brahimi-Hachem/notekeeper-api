from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.health import router as health_router
from app.api.routers.notes import router as notes_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="NoteKeeper API",
    version="0.1.0",
    description="Backend API for storing and retrieving personal notes.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(notes_router)
app.include_router(auth_router)
