from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from api.config.database import Base
from api.exceptions import DatabaseException
from api.repositories.note_repository import SQLAlchemyNoteRepository
from api.schemas import (
    DeadlineFilterSchema,
    NoteCreateData,
    NoteUpdateData,
    StatusFilterSchema,
)

tz = timezone.utc


class TestSQLAlchemyNoteRepository:

    @pytest.fixture(autouse=True)
    def _setup_database(self):
        """Prepare a clean SQLite database in memory before each test."""
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(bind=engine)
        testing_session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        self.db_session: Session = testing_session_local()
        self.repository = SQLAlchemyNoteRepository(session=self.db_session)

        yield

        self.db_session.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_note_success(self):
        note_data: NoteCreateData = {
            "title": "Note Test",
            "content": "Content Test",
            "deadline": date(2030, 12, 31),
        }

        created_note = self.repository.create_note(note_data)

        assert created_note.id is not None
        assert created_note.title == note_data["title"]
        assert created_note.content == note_data["content"]
        assert created_note.is_done is False
        assert created_note.deadline == note_data["deadline"]

    def test_get_note_by_id_returns_note_when_exists(self):
        note_data: NoteCreateData = {"title": "Note data", "content": "Note details"}
        created_note = self.repository.create_note(note_data)

        found_note = self.repository.get_note_by_id(created_note.id)

        assert found_note is not None
        assert found_note.id == created_note.id
        assert found_note.title == note_data["title"]

    def test_get_note_by_id_returns_none_when_not_exists(self):
        found_note = self.repository.get_note_by_id(999)

        assert found_note is None

    def test_update_note_success(self):
        created_note = self.repository.create_note(
            {"title": "Orginal", "content": "Original text"}
        )
        update_data: NoteUpdateData = {
            "title": "Updated",
            "content": "Updated text",
            "is_done": True,
            "deadline": None,
        }

        updated_note = self.repository.update_note(created_note.id, update_data)

        assert updated_note is not None
        assert updated_note.title == update_data["title"]
        assert updated_note.content == update_data["content"]
        assert updated_note.is_done is True

    def test_update_note_returns_none_when_not_exists(self):
        update_data: NoteUpdateData = {
            "title": "Updated",
            "content": "Content text",
            "is_done": True,
            "deadline": None,
        }

        result = self.repository.update_note(999, update_data)

        assert result is None

    def test_change_note_status_success(self):
        created_note = self.repository.create_note(
            {"title": "Note title", "content": "Note text"}
        )

        updated_note = self.repository.change_note_status(
            created_note.id, is_done=True
        )

        assert updated_note is not None
        assert updated_note.is_done is True

    def test_change_note_status_returns_none_when_not_exists(self):
        result = self.repository.change_note_status(999, is_done=True)

        assert result is None

    def test_delete_note_success(self):
        created_note = self.repository.create_note(
            {"title": "Note content", "content": "Note content"}
        )

        deleted = self.repository.delete_note(created_note.id)

        assert deleted is True
        assert self.repository.get_note_by_id(created_note.id) is None

    def test_delete_note_returns_false_when_not_exists(self):
        deleted = self.repository.delete_note(999)

        assert deleted is False

    def test_get_notes_without_filters_returns_all(self):
        self.repository.create_note({"title": "Note 1", "content": "Content 1"})
        self.repository.create_note({"title": "Note 2", "content": "Content 2"})

        notes = self.repository.get_notes(filters=None)

        assert len(notes) == 2

    def test_get_notes_filter_by_status(self):
        note_pending = self.repository.create_note(
            {"title": "Pending note", "content": "Pending content"}
        )
        note_done = self.repository.create_note({"title": "Done note", "content": "Done content"})
        self.repository.change_note_status(note_done.id, is_done=True)

        done_notes = self.repository.get_notes(
            filters={"status": StatusFilterSchema.DONE}
        )
        pending_notes = self.repository.get_notes(
            filters={"status": StatusFilterSchema.PENDING}
        )

        assert len(done_notes) == 1
        assert done_notes[0].id == note_done.id

        assert len(pending_notes) == 1
        assert pending_notes[0].id == note_pending.id

    def test_get_notes_filter_by_deadline(self):
        today = datetime.now(tz).date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        note_expired = self.repository.create_note(
            {"title": "Expired note", "content": "Expired content", "deadline": yesterday}
        )
        note_pending = self.repository.create_note(
            {"title": "Future note", "content": "Future content", "deadline": tomorrow}
        )
        self.repository.create_note(
            {"title": "No deadline note", "content": "No deadline content", "deadline": None}
        )

        expired_notes = self.repository.get_notes(
            filters={"deadline": DeadlineFilterSchema.EXPIRED}
        )
        pending_notes = self.repository.get_notes(
            filters={"deadline": DeadlineFilterSchema.PENDING}
        )

        assert len(expired_notes) == 1
        assert expired_notes[0].id == note_expired.id

        assert len(pending_notes) == 1
        assert pending_notes[0].id == note_pending.id

    def test_create_note_raises_database_exception_on_sqlalchemy_error(self):
        mock_session = MagicMock(spec=Session)
        mock_session.add.side_effect = SQLAlchemyError("Error de conexion SQL")
        repo = SQLAlchemyNoteRepository(session=mock_session)

        with pytest.raises(DatabaseException) as exc_info:
            repo.create_note({"title": "Test", "content": "Test"})

        assert "Failed to create note" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
