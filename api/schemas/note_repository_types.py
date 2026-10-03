from datetime import date
from typing import TypedDict


class NoteCreateData(TypedDict):
    content: str
    deadline: date | None

class NoteUpdateData(NoteCreateData):
    is_done: bool
