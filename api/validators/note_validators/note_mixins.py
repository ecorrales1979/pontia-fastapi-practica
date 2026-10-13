from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TitleMixin(BaseModel):
    title: str = Field(
            ...,
            min_length=1,
            description="Title must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)

class ContentMixin(BaseModel):
    content: str = Field(
            ...,
            min_length=1,
            description="Content must not be empty"
        )

    model_config = ConfigDict(str_strip_whitespace=True)

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
