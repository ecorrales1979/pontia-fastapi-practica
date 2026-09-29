from fastapi import APIRouter

from api.services import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])
service = NoteService()

@router.get("/")
def list_notes():
    return service.list()

@router.get("/{note_id}")
def show_note(note_id: int):
    return service.get(note_id)
