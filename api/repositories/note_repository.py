from sqlalchemy.exc import SQLAlchemyError

from api.config.database import SessionLocal
from api.exceptions import DatabaseException
from api.models import NoteModel
from api.schemas import NoteCreateData, NoteUpdateData


class NoteRepository:
    def get_notes(self) -> list[NoteModel]:
        with SessionLocal() as db:
            try:
                return db.query(NoteModel).all()
            except SQLAlchemyError as exc:
                raise DatabaseException("Failed to list notes", exc) from exc

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        with SessionLocal() as db:
            try:
                return db.query(NoteModel).filter(NoteModel.id == note_id).first()
            except SQLAlchemyError as exc:
                raise DatabaseException("Failed to get note by id", exc) from exc

    def create_note(self, note_data: NoteCreateData) -> NoteModel:
        with SessionLocal() as db:
            try:
                new_note = NoteModel(**note_data)
                db.add(new_note)
                db.commit()
                db.refresh(new_note)
                return new_note
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to create note", exc) from exc

    def update_note(self, note_id: int, note_data: NoteUpdateData) -> NoteModel | None:
        with SessionLocal() as db:
            try:
                note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
                if not note:
                    return None
                for key, value in note_data.items():
                    setattr(note, key, value)
                db.commit()
                db.refresh(note)
                return note
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to update note", exc) from exc

    def change_note_status(self, note_id: int, is_done: bool) -> NoteModel | None:
        with SessionLocal() as db:
            try:
                note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
                if not note:
                    return None
                note.is_done = is_done
                db.commit()
                db.refresh(note)
                return note
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to change note status", exc) from exc

    def delete_note(self, note_id: int) -> bool:
        with SessionLocal() as db:
            try:
                note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
                if not note:
                    return False
                db.delete(note)
                db.commit()
                return True
            except SQLAlchemyError as exc:
                db.rollback()
                raise DatabaseException("Failed to delete note", exc) from exc
