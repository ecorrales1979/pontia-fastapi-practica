from api.config.database import SessionLocal
from api.models import NoteModel


class NoteRepository:
    def get_notes(self) -> list[NoteModel]:
        with SessionLocal() as db:
            return db.query(NoteModel).all()

    def get_note_by_id(self, note_id: int) -> NoteModel | None:
        with SessionLocal() as db:
            return db.query(NoteModel).filter(NoteModel.id == note_id).first()
