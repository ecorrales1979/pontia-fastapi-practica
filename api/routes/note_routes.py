from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.config.dependencies.note_dependencies import get_note_service
from api.schemas import DeadlineQuery, NoteFilterParams, StatusQuery
from api.services import NoteService
from api.utils.logger import Logger
from api.validators.note_validators import (
    NoteCreateValidator,
    NoteSetDoneValidator,
    NoteUpdateValidator,
)

logger = Logger()

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(get_note_service)]
)

NoteServiceDependency = Annotated[NoteService, Depends(get_note_service)]

@router.get("/")
def list_notes(
    service: NoteServiceDependency,
    deadline: DeadlineQuery = None,
    status: StatusQuery = None
):
    filters: NoteFilterParams = {}
    if deadline is not None:
        filters["deadline"] = deadline
    if status is not None:
        filters["status"] = status

    notes_list = service.list(filters=filters if filters else None)
    logger.info(f"Notas listadas con éxito. Cantidad: {len(notes_list)}", context={"filters": filters})
    return notes_list


@router.get("/{note_id}")
def show_note(note_id: int, service: NoteServiceDependency):
    note = service.show(note_id)
    logger.info(f"Nota obtenida con éxito. ID: {note_id}")
    return note


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreateValidator, service: NoteServiceDependency):
    created_note = service.create(payload)
    logger.info("Nota creada con éxito.", context={"note": created_note})
    return created_note


@router.put("/{note_id}")
def update_note(
    note_id: int,
    payload: NoteUpdateValidator,
    service: NoteServiceDependency
):
    updated_note = service.update(note_id, payload)
    logger.info("Nota actualizada con éxito.", context={"note": updated_note})
    return updated_note


@router.patch("/{note_id}/done")
def change_note_status(
    note_id: int,
    payload: NoteSetDoneValidator,
    service: NoteServiceDependency
):
    updated_note = service.change_status(note_id=note_id, is_done=payload.is_done)
    logger.info("Status de la nota actualizado con éxito.", context={"note": updated_note})
    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, service: NoteServiceDependency):
    was_deleted = service.delete(note_id)
    logger.info("Nota eliminada con éxito.", context={"note_id": note_id})
    return was_deleted
