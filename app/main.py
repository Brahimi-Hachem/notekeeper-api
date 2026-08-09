from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.notes import router as notes_router

app = FastAPI(
    title="NoteKeeper API",
    version="0.1.0",
    description="Backend API for storing and retrieving personal notes.",
)

app.include_router(health_router)
app.include_router(notes_router)
