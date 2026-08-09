from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Note
from app.db.session import get_db
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate, db: DatabaseSession) -> Note:
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/", response_model=list[NoteResponse])
def list_notes(db: DatabaseSession) -> list[Note]:
    statement = select(Note).order_by(Note.id)
    return list(db.scalars(statement))
