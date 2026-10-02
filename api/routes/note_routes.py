from fastapi import APIRouter

from api.services import NoteService
from api.validators.note_create_validator import NoteCreateValidator

router = APIRouter(prefix="/notes", tags=["Notes"])
service = NoteService()

@router.get("/")
def list_notes():
    return service.list()

@router.get("/{note_id}")
def show_note(note_id: int):
    return service.show(note_id)

@router.post("/")
def create_note(payload: NoteCreateValidator):
    return service.create(payload)
