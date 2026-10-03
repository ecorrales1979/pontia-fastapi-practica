from pydantic import Field

from .note_create_validator import NoteCreateValidator


class NoteUpdateValidator(NoteCreateValidator):
    is_done: bool = Field(
        False,
        description="Indicates whether the note is done"
    )
