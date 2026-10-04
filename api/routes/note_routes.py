from fastapi import APIRouter

from api.services import NoteService
from api.validators.note_validators import (
    NoteCreateValidator,
    NoteSetDoneValidator,
    NoteUpdateValidator,
)

router = APIRouter(prefix="/notes", tags=["Notes"])
service = NoteService()

@router.get("/")
def list_notes():
    return service.list()

@router.get("/{note_id}")
def show_note(note_id: int):
    return service.show(note_id)

@router.post("/", status_code=201)
def create_note(payload: NoteCreateValidator):
    return service.create(payload)

@router.put("/{note_id}")
def update_note(note_id: int, payload: NoteUpdateValidator):
    return service.update(note_id, payload)

@router.patch("/{note_id}/done")
def change_note_status(note_id: int, payload: NoteSetDoneValidator):
    return service.change_status(note_id=note_id, is_done=payload.is_done)
