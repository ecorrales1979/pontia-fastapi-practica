from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.config.dependencies.note_dependencies import get_note_service
from api.services import NoteService
from api.validators.note_validators import (
    NoteCreateValidator,
    NoteSetDoneValidator,
    NoteUpdateValidator,
)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(get_note_service)]
)

NoteServiceDependency = Annotated[NoteService, Depends(get_note_service)]


@router.get("/")
def list_notes(service: NoteServiceDependency):
    return service.list()


@router.get("/{note_id}")
def show_note(note_id: int, service: NoteServiceDependency):
    return service.show(note_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreateValidator, service: NoteServiceDependency):
    return service.create(payload)


@router.put("/{note_id}")
def update_note(
    note_id: int,
    payload: NoteUpdateValidator,
    service: NoteServiceDependency
):
    return service.update(note_id, payload)


@router.patch("/{note_id}/done")
def change_note_status(
    note_id: int,
    payload: NoteSetDoneValidator,
    service: NoteServiceDependency
):
    return service.change_status(note_id=note_id, is_done=payload.is_done)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, service: NoteServiceDependency):
    return service.delete(note_id)
