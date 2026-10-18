from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class TitleMixin(BaseModel):
    title: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=1, description="Title must not be empty")
    ]

class ContentMixin(BaseModel):
    content: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=1, description="Content must not be empty")
    ]

class DeadlineMixin(BaseModel):
    deadline: Annotated[
        date | None,
        Field(default=None, description="Deadline must be in YYYY-MM-DD format")
    ]

class IsDoneMixin(BaseModel):
    is_done: Annotated[
        bool,
        Field(description="Indicates whether the note is done")
    ]
