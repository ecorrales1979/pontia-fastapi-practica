from pydantic import BaseModel, Field


class NoteDoneChangeValidator(BaseModel):
    is_done: bool = Field(
        False,
        description="Indicates whether the note is done"
    )
