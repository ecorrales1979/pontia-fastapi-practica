from typing import Protocol

from api.models import NoteModel
from api.schemas import NoteCreateData, NoteUpdateData


class NoteRepositoryInterface(Protocol):
    def get_notes(self) -> list[NoteModel]:
        ...

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        ...

    def create_note(self, note_data: NoteCreateData) -> NoteModel:
        ...

    def update_note(self, note_id: int, note_data: NoteUpdateData) -> NoteModel | None:
        ...

    def change_note_status(self, note_id: int, is_done: bool) -> NoteModel | None:
        ...

    def delete_note(self, note_id: int) -> bool:
        ...
