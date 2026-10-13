from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

# from fastapi.testclient import TestClient
from starlette.testclient import TestClient

from api.config.dependencies.note_dependencies import get_note_service
from api.exceptions import (
    BusinessException,
    DatabaseException,
    DomainException,
    ResourceNotFoundException,
)
from api.main import app
from api.models import NoteModel
from api.services import NoteService

tz=timezone.utc


class TestNoteRoutes:

    @pytest.fixture(autouse=True)
    def _setup_api_client(self):
        """Mockea la instancia de NoteService e inyecta la dependencia en FastAPI."""
        self.mock_service = Mock(spec=NoteService)

        # Prevents FastAPI jsonable_encoder from entering into an
        # infinite recursion when serializing the mock service
        self.mock_service.__dataclass_fields__ = None
        self.mock_service.__pydantic_model__ = None
        self.mock_service.__get_pydantic_core_schema__ = None

        app.dependency_overrides[get_note_service] = lambda: self.mock_service
        self.client = TestClient(app)

        yield

        # Clean overrides to avoid contamination between tests
        app.dependency_overrides.clear()

    # =========================================================================
    # 1. GET /notes/ (list_notes)
    # =========================================================================

    def test_list_notes_success_without_filters(self):
        fake_note = NoteModel(id=1, title="Note 1", content="Text 1", is_done=False)
        self.mock_service.list.return_value = [fake_note]

        response = self.client.get("/notes/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        self.mock_service.list.assert_called_once_with(filters=None)

    def test_list_notes_success_with_query_filters(self):
        self.mock_service.list.return_value = []

        response = self.client.get("/notes/?status=pending&deadline=expired")

        assert response.status_code == 200
        self.mock_service.list.assert_called_once_with(
            filters={"deadline": "expired", "status": "pending"}
        )

    def test_list_notes_database_error_returns_500(self):
        self.mock_service.list.side_effect = DatabaseException(
            "Failed to list notes", Exception("DB connection timeout")
        )

        response = self.client.get("/notes/")

        assert response.status_code == 500

    # =========================================================================
    # 2. GET /notes/{note_id} (show_note)
    # =========================================================================

    def test_show_note_success(self):
        fake_note = NoteModel(id=5, title="Note 5", content="Text 5", is_done=False)
        self.mock_service.show.return_value = fake_note

        response = self.client.get("/notes/5")

        assert response.status_code == 200
        assert response.json()["id"] == 5
        self.mock_service.show.assert_called_once_with(5)

    def test_show_note_not_found_returns_404(self):
        self.mock_service.show.side_effect = ResourceNotFoundException(
            resource_name="Note", resource_id=999
        )

        response = self.client.get("/notes/999")

        assert response.status_code == 404
        self.mock_service.show.assert_called_once_with(999)

    def test_show_note_invalid_path_param_returns_422(self):
        response = self.client.get("/notes/abc")

        assert response.status_code == 422
        self.mock_service.show.assert_not_called()

    # =========================================================================
    # 3. POST /notes/ (create_note)
    # =========================================================================

    def test_create_note_success_returns_201(self):
        future_date = (datetime.now(tz=tz).date() + timedelta(days=5)).isoformat()
        fake_note = NoteModel(id=1, title="New note", content="Note content", is_done=False)
        self.mock_service.create.return_value = fake_note

        payload = {
            "title": "  New Note  ",
            "content": "Note content",
            "deadline": future_date,
        }

        response = self.client.post("/notes/", json=payload)

        assert response.status_code == 201
        assert response.json()["id"] == 1
        self.mock_service.create.assert_called_once()

    def test_create_note_pydantic_validation_error_returns_422(self):
        payload = {"title": "", "content": "Note content"}

        response = self.client.post("/notes/", json=payload)

        assert response.status_code == 422
        self.mock_service.create.assert_not_called()

    def test_create_note_business_exception_returns_409(self):
        past_date = (datetime.now(tz=tz).date() - timedelta(days=5)).isoformat()
        self.mock_service.create.side_effect = BusinessException(
            "The deadline cannot be in the past."
        )
        payload = {"title": "Note title", "content": "Note content", "deadline": past_date}

        response = self.client.post("/notes/", json=payload)

        assert response.status_code == 409
        self.mock_service.create.assert_called_once()

    # =========================================================================
    # 4. PUT /notes/{note_id} (update_note)
    # =========================================================================

    def test_update_note_success(self):
        fake_note = NoteModel(id=2, title="Note title", content="Note content", is_done=True)
        self.mock_service.update.return_value = fake_note

        payload = {
            "title": "Note title",
            "content": "Note content",
            "is_done": True,
            "deadline": None,
        }

        response = self.client.put("/notes/2", json=payload)

        assert response.status_code == 200
        assert response.json()["title"] == payload["title"]
        self.mock_service.update.assert_called_once()

    def test_update_note_not_found_returns_404(self):
        self.mock_service.update.side_effect = ResourceNotFoundException(
            resource_name="Note", resource_id=999
        )
        payload = {
            "title": "Note title",
            "content": "Note content",
            "is_done": True,
            "deadline": None,
        }

        response = self.client.put("/notes/999", json=payload)

        assert response.status_code == 404
        self.mock_service.update.assert_called_once()

    def test_update_note_pydantic_validation_error_returns_422(self):
        payload = {"title": "Note title", "content": "Note content", "is_done": "ABC"}

        response = self.client.put("/notes/1", json=payload)

        assert response.status_code == 422
        self.mock_service.update.assert_not_called()

    # =========================================================================
    # 5. PATCH /notes/{note_id}/done (change_note_status)
    # =========================================================================

    def test_change_note_status_success(self):
        fake_note = NoteModel(id=1, title="Note title", content="Note content", is_done=True)
        self.mock_service.change_status.return_value = fake_note

        payload = {"is_done": True}

        response = self.client.patch("/notes/1/done", json=payload)

        assert response.status_code == 200
        assert response.json()["is_done"] is True
        self.mock_service.change_status.assert_called_once_with(note_id=1, is_done=True)

    def test_change_note_status_not_found_returns_404(self):
        self.mock_service.change_status.side_effect = ResourceNotFoundException(
            resource_name="Note", resource_id=999
        )

        response = self.client.patch("/notes/999/done", json={"is_done": True})

        assert response.status_code == 404
        self.mock_service.change_status.assert_called_once_with(note_id=999, is_done=True)

    def test_change_note_status_validation_error_returns_422(self):
        response = self.client.patch("/notes/1/done", json={"is_done": "ABC"})

        assert response.status_code == 422
        self.mock_service.change_status.assert_not_called()

    # =========================================================================
    # 6. DELETE /notes/{note_id} (delete_note)
    # =========================================================================

    def test_delete_note_success_returns_204(self):
        self.mock_service.delete.return_value = True

        response = self.client.delete("/notes/1")

        assert response.status_code == 204
        assert response.content == b""
        self.mock_service.delete.assert_called_once_with(1)

    def test_delete_note_not_found_returns_404(self):
        self.mock_service.delete.side_effect = ResourceNotFoundException(
            resource_name="Note", resource_id=999
        )

        response = self.client.delete("/notes/999")

        assert response.status_code == 404
        self.mock_service.delete.assert_called_once_with(999)

    def test_delete_note_database_error_returns_500(self):
        self.mock_service.delete.side_effect = DatabaseException(
            "Failed to delete note", Exception("FK Constraint violation")
        )

        response = self.client.delete("/notes/1")

        assert response.status_code == 500
        self.mock_service.delete.assert_called_once_with(1)
