from datetime import datetime, timedelta, timezone

import pytest

from api.exceptions import BusinessException, ResourceNotFoundException
from api.repositories.note_repository.fake_note_repository import FakeNoteRepository
from api.services.note_service import NoteService
from tests.mocks.note_mocks import DummyCreateValidator, DummyUpdateValidator

tz = timezone.utc


@pytest.fixture
def fake_repo() -> FakeNoteRepository:
    """Fixture que proporciona un FakeNoteRepository totalmente limpio en cada test (beforeEach)."""
    return FakeNoteRepository()


@pytest.fixture
def note_service(fake_repo: FakeNoteRepository) -> NoteService:
    """Fixture que instancia el NoteService inyectándole el Fake Repository."""
    return NoteService(repository=fake_repo)


class TestNoteService:
    @pytest.fixture(autouse=True)
    def _setup_service(self):
        self.fake_repo = FakeNoteRepository()
        self.note_service = NoteService(repository=self.fake_repo)

    def test_list_notes_returns_notes_from_repository(self):
        # Setup (BeforeEach específico)
        self.fake_repo.create_note({"title": "Nota 1", "content": "Contenido 1"})
        self.fake_repo.create_note({"title": "Nota 2", "content": "Contenido 2"})

        notes = self.note_service.list(filters={})

        assert len(notes) == 2
        assert notes[0].title == "Nota 1"
        assert notes[1].title == "Nota 2"

    def test_show_note_success(self):
        created_note = self.fake_repo.create_note(
            {"title": "Nota Existente", "content": "XYZ"}
        )

        note = self.note_service.show(note_id=created_note.id)

        assert note.id == created_note.id
        assert note.title == "Nota Existente"

    def test_show_note_raises_resource_not_found_when_not_exists(self):
        with pytest.raises(ResourceNotFoundException) as exc_info:
            self.note_service.show(note_id=999)

        print(exc_info)

        assert "Note with id 999 not found" in str(exc_info.value)

    def test_create_note_success(self):
        future_date = datetime.now(tz).date() + timedelta(days=5)
        validator = DummyCreateValidator(
            title="Nota nueva",
            content="Contenido escrito por un tonto",
            deadline=future_date,
        )

        created_note = self.note_service.create(validator)

        assert created_note.id == 1
        assert created_note.title == "Nota nueva"
        assert created_note.content == "Contenido escrito por un *****"
        assert created_note.deadline == future_date

    def test_create_note_raises_business_exception_if_deadline_is_past(self):
        past_date = datetime.now(tz).date() - timedelta(days=1)
        validator = DummyCreateValidator(
            title="Nota Vencida", content="ABC", deadline=past_date
        )

        with pytest.raises(BusinessException) as exc_info:
            self.note_service.create(validator)

        assert "The deadline cannot be in the past." in str(exc_info.value)

    def test_update_note_success(self):
        created_note = self.fake_repo.create_note(
            {"title": "Título Viejo", "content": "Viejo"}
        )
        update_data = DummyUpdateValidator(
            title="Título Nuevo",
            content="Nuevo contenido",
            is_done=True,
            deadline=None,
        )

        updated_note = self.note_service.update(
            note_id=created_note.id, note_data=update_data
        )

        assert updated_note.title == "Título Nuevo"
        assert updated_note.content == "Nuevo contenido"
        assert updated_note.is_done is True

    def test_update_note_raises_business_exception_if_deadline_is_past(self):
        created_note = self.fake_repo.create_note(
            {"title": "Nota Real", "content": "Texto"}
        )
        past_date = datetime.now(tz).date() - timedelta(days=2)
        update_data = DummyUpdateValidator(
            title="Update Inválido",
            content="Texto",
            is_done=False,
            deadline=past_date,
        )

        with pytest.raises(BusinessException) as exc_info:
            self.note_service.update(note_id=created_note.id, note_data=update_data)

        assert "The deadline cannot be in the past." in str(exc_info.value)

    def test_update_note_raises_resource_not_found_when_not_exists(self):
        update_data = DummyUpdateValidator(title="N/A", content="N/A", is_done=False)

        with pytest.raises(ResourceNotFoundException) as exc_info:
            self.note_service.update(note_id=999, note_data=update_data)

        assert "Note with id 999 not found" in str(exc_info.value)

    def test_change_status_success(self):
        created_note = self.fake_repo.create_note(
            {"title": "Nota Incompleta", "content": "123"}
        )

        updated_note = self.note_service.change_status(
            note_id=created_note.id, is_done=True
        )

        assert updated_note.is_done is True

    def test_change_status_raises_resource_not_found_when_not_exists(self):
        with pytest.raises(ResourceNotFoundException) as exc_info:
            self.note_service.change_status(note_id=999, is_done=True)

        assert "Note with id 999 not found" in str(exc_info.value)

    def test_delete_note_success(self):
        created_note = self.fake_repo.create_note(
            {"title": "A borrar", "content": "123"}
        )

        result = self.note_service.delete(note_id=created_note.id)

        assert result is True
        assert len(self.fake_repo.notes) == 0

    def test_delete_note_raises_resource_not_found_when_not_exists(self):
        with pytest.raises(ResourceNotFoundException) as exc_info:
            self.note_service.delete(note_id=999)

        assert "Note with id 999 not found" in str(exc_info.value)
