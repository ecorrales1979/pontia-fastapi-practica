from datetime import date


class DummyCreateValidator:
    def __init__(self, title: str, content: str, deadline: date | None = None) -> None:
        self.title = title
        self.content = content
        self.deadline = deadline


class DummyUpdateValidator:
    def __init__(self, title: str, content: str, is_done: bool, deadline: date | None = None) -> None:
        self.title = title
        self.content = content
        self.is_done = is_done
        self.deadline = deadline
