from typing import Annotated, TypeAlias

from fastapi import Depends

from api.config.database import DBSessionDependency
from api.repositories.note_repository import (
    NoteRepositoryInterface,
    SQLAlchemyNoteRepository,
)
from api.services.note_service import NoteService


def get_note_repository(db: DBSessionDependency) -> NoteRepositoryInterface:
    return SQLAlchemyNoteRepository(session=db)

NoteRepositoryDependency: TypeAlias = Annotated[NoteRepositoryInterface, Depends(get_note_repository)]

def get_note_service(repository: NoteRepositoryDependency) -> NoteService:
    return NoteService(note_repository=repository)
