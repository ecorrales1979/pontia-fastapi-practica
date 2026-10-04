from api.exceptions import ResourceNotFoundException
from api.models import NoteModel
from api.repositories import NoteRepository
from api.validators.note_validators import NoteCreateValidator, NoteUpdateValidator


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

    def create(self, note_data: NoteCreateValidator) -> NoteModel:
        return self.repository.create_note({
            "content": note_data.content,
            "deadline": note_data.deadline or None
        })

    def update(self, note_id: int, note_data: NoteUpdateValidator) -> NoteModel:
        note = self.repository.update_note(note_id, {
            "content": note_data.content,
            "deadline": note_data.deadline or None,
            "is_done": note_data.is_done
        })
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note

    def change_status(self, note_id: int, is_done: bool) -> NoteModel:
        note = self.repository.change_note_status(note_id, is_done)
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note
