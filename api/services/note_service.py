from api.exceptions import ResourceNotFoundException
from api.models import NoteModel
from api.repositories import NoteRepository


class NoteService:
    def __init__(self):
        self.repository = NoteRepository()

    def list(self) -> list[NoteModel]:
        return self.repository.get_notes()

    def show(self, note_id: int) -> NoteModel:
        note = self.repository.get_note_by_id(note_id)
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note
