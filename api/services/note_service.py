from api.models import NoteModel
from api.repositories import NoteRepository


class NoteService:
    def __init__(self):
        self.repository = NoteRepository()

    def list(self) -> list[NoteModel]:
        return self.repository.get_notes()

    def get(self, note_id: int) -> NoteModel | None:
        return self.repository.get_note_by_id(note_id)
