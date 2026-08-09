from fastapi import APIRouter

from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate) -> NoteResponse:
    return NoteResponse(
        id=1,
        title=note.title,
        content=note.content,
    )
