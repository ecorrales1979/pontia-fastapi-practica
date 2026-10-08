from api.exceptions import BusinessException, ResourceNotFoundException
from api.models import NoteModel
from api.repositories.note_repository import NoteRepositoryInterface
from api.schemas import NoteFilterParams
from api.utils import DateUtils, TextUtils
from api.validators.note_validators import NoteCreateValidator, NoteUpdateValidator


class NoteService:
    def __init__(self, repository: NoteRepositoryInterface) -> None:
        self._repository = repository

    def list(self, filters: NoteFilterParams) -> list[NoteModel]:
        return self._repository.get_notes(filters)

    def show(self, note_id: int) -> NoteModel:
        note = self._repository.get_note_by_id(note_id)
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note

    def create(self, note_data: NoteCreateValidator) -> NoteModel:
        if note_data.deadline and DateUtils.is_past_date(note_data.deadline):
            raise BusinessException("The deadline cannot be in the past.")

        return self._repository.create_note({
            "title": TextUtils.sanitize_text(note_data.title),
            "content": TextUtils.sanitize_text(note_data.content),
            "deadline": note_data.deadline or None
        })

    def update(self, note_id: int, note_data: NoteUpdateValidator) -> NoteModel:
        if note_data.deadline and DateUtils.is_past_date(note_data.deadline):
            raise BusinessException("The deadline cannot be in the past.")

        note = self._repository.update_note(note_id, {
            "title": TextUtils.sanitize_text(note_data.title),
            "content": TextUtils.sanitize_text(note_data.content),
            "deadline": note_data.deadline or None,
            "is_done": note_data.is_done
        })
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note

    def change_status(self, note_id: int, is_done: bool) -> NoteModel:
        note = self._repository.change_note_status(note_id, is_done)
        if not note:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return note

    def delete(self, note_id: int) -> bool:
        was_deleted = self._repository.delete_note(note_id)
        if not was_deleted:
            raise ResourceNotFoundException(resource_name="Note", resource_id=note_id)
        return True
