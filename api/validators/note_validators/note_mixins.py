from datetime import date

from pydantic import BaseModel, Field


class ContentMixin(BaseModel):
    content: str = Field(
            ...,
            min_length=1,
            strip_whitespace=True,
            description="Content must not be empty"
        )

class DeadlineMixin(BaseModel):
    deadline: date | None = Field(
            None,
            description="Deadline must be in YYYY-MM-DD format"
        )

class IsDoneMixin(BaseModel):
    is_done: bool = Field(
        False,
        description="Indicates whether the note is done"
    )
