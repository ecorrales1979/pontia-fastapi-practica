from api.config.database import SessionLocal
from api.models import NoteModel
from api.schemas import NoteCreateData, NoteUpdateData


class NoteRepository:
    def get_notes(self) -> list[NoteModel]:
        with SessionLocal() as db:
            return db.query(NoteModel).all()

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        with SessionLocal() as db:
            return db.query(NoteModel).filter(NoteModel.id == note_id).first()

    def create_note(self, note_data: NoteCreateData) -> NoteModel:
        with SessionLocal() as db:
            new_note = NoteModel(**note_data)
            db.add(new_note)
            db.commit()
            db.refresh(new_note)
            return new_note

    def update_note(self, note_id: int, note_data: NoteUpdateData) -> NoteModel | None:
        with SessionLocal() as db:
            note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
            if not note:
                return None
            for key, value in note_data.items():
                setattr(note, key, value)
            db.commit()
            db.refresh(note)
            return note

    def change_note_status(self, note_id: int, is_done: bool) -> NoteModel | None:
        with SessionLocal() as db:
            note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
            if not note:
                return None
            note.is_done = is_done
            db.commit()
            db.refresh(note)
            return note
