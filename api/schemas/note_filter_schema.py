from enum import Enum
from typing import Annotated, TypedDict

from fastapi import Query


class DeadlineFilterSchema(str, Enum):
    EXPIRED = "expired"
    PENDING = "pending"


class StatusFilterSchema(str, Enum):
    DONE = "done"
    PENDING = "pending"


class NoteFilterParams(TypedDict):
    deadline: DeadlineFilterSchema | None
    status: StatusFilterSchema | None


DeadlineQuery = Annotated[
    DeadlineFilterSchema | None,
    Query(description="Filter notes by their deadline status."),
]

StatusQuery = Annotated[
    StatusFilterSchema | None,
    Query(description="Filter notes by their completion status."),
]
