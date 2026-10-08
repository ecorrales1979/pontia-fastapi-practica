from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.exceptions import DatabaseException
from api.models import NoteModel
from api.schemas import NoteCreateData, NoteUpdateData

from .note_repository_interface import NoteRepositoryInterface  # noqa: F401


class SQLAlchemyNoteRepository:

    def __init__(self, session: Session):
        self._db = session

    def get_notes(self) -> list[NoteModel]:
        try:
            return self._db.query(NoteModel).all()
        except SQLAlchemyError as exc:
            raise DatabaseException("Failed to list notes", exc) from exc

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        try:
            return self._db.query(NoteModel).filter(NoteModel.id == note_id).first()
        except SQLAlchemyError as exc:
            raise DatabaseException("Failed to get note by id", exc) from exc

    def create_note(self, note_data: NoteCreateData) -> NoteModel:
        try:
            new_note = NoteModel(**note_data)
            self._db.add(new_note)
            self._db.commit()
            self._db.refresh(new_note)
            return new_note
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to create note", exc) from exc

    def update_note(self, note_id: int, note_data: NoteUpdateData) -> NoteModel | None:
        try:
            note = self._db.query(NoteModel).filter(NoteModel.id == note_id).first()
            if not note:
                return None

            for key, value in note_data.items():
                setattr(note, key, value)

            self._db.commit()
            self._db.refresh(note)
            return note
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to update note", exc) from exc

    def change_note_status(self, note_id: int, is_done: bool) -> NoteModel | None:
        try:
            note = self._db.query(NoteModel).filter(NoteModel.id == note_id).first()
            if not note:
                return None

            note.is_done = is_done
            self._db.commit()
            self._db.refresh(note)
            return note
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to change note status", exc) from exc

    def delete_note(self, note_id: int) -> bool:
        try:
            note = self._db.query(NoteModel).filter(NoteModel.id == note_id).first()
            if not note:
                return False

            self._db.delete(note)
            self._db.commit()
            return True
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise DatabaseException("Failed to delete note", exc) from exc
