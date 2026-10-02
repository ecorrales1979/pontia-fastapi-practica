from datetime import date

from pydantic import BaseModel, Field


class NoteCreateValidator(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        strip_whitespace=True,
        description="Content must not be empty"
    )
    deadline: date | None = Field(
        None,
        description="Deadline must be in YYYY-MM-DD format"
    )
