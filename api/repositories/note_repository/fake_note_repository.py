from api.models import NoteModel
from api.schemas import NoteCreateData, NoteFilterParams, NoteUpdateData

from .note_repository_interface import NoteRepositoryInterface


class FakeNoteRepository(NoteRepositoryInterface):
    def __init__(self):
        self.notes = []
        self._next_id = 1

    def get_notes(self, filters: NoteFilterParams = None):
        return self.notes

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def create_note(self, note_data: NoteCreateData):
        note = NoteModel(
            id=self._next_id,
            title=note_data["title"],
            content=note_data["content"],
            deadline=note_data.get("deadline"),
            is_done=False,
        )
        self.notes.append(note)
        self._next_id += 1
        return note

    def update_note(self, note_id, note_data: NoteUpdateData):
        note = self.get_note_by_id(note_id)
        if not note:
            return None
        for field, value in note_data.items():
            setattr(note, field, value)
        return note

    def change_note_status(self, note_id: int, is_done: bool) -> NoteModel | None:
        note = self.get_note_by_id(note_id)
        if not note:
            return None
        note.is_done = is_done
        return note

    def delete_note(self, note_id: int) -> bool:
        note = self.get_note_by_id(note_id)
        if not note:
            return False
        self.notes.remove(note)
        return True
