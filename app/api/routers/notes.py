from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.models import Note, User
from app.db.session import get_db
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(
    note: NoteCreate,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> Note:
    db_note = Note(
        **note.model_dump(),
        user_id=current_user.id,
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    db: DatabaseSession,
    current_user: CurrentUser,
) -> list[Note]:
    statement = select(Note).where(Note.user_id == current_user.id).order_by(Note.id)

    return list(db.scalars(statement))


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> Note:
    statement = select(Note).where(
        Note.id == note_id,
        Note.user_id == current_user.id,
    )

    note = db.scalar(statement)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> Note:
    statement = select(Note).where(
        Note.id == note_id,
        Note.user_id == current_user.id,
    )

    note = db.scalar(statement)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.title = note_data.title
    note.content = note_data.content

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> None:
    statement = select(Note).where(
        Note.id == note_id,
        Note.user_id == current_user.id,
    )

    note = db.scalar(statement)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()
