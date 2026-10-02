from api.config.database import SessionLocal
from api.models import NoteModel
from api.schemas import NoteCreateData


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
