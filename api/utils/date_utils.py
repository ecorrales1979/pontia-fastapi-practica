from datetime import date, datetime, timezone
from typing import TypeAlias

DateInput: TypeAlias = date | datetime | str


class DateUtils:

    @staticmethod
    def get_today() -> date:
        return datetime.now(timezone.utc).date()

    @staticmethod
    def to_date(value: DateInput) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            return date.fromisoformat(value)
        raise ValueError(f"Unsupported type for conversion to date: {type(value)}. Allowed types are date, datetime, and str.")

    @classmethod
    def days_difference(cls, target_date: DateInput, reference_date: DateInput | None = None) -> int:
        parsed_target_date = cls.to_date(target_date)
        today = cls.get_today() if reference_date is None else cls.to_date(reference_date)
        return (parsed_target_date - today).days

    @classmethod
    def is_future_date(cls, deadline: DateInput, reference_date: DateInput | None = None) -> bool:
        return cls.days_difference(deadline, reference_date) > 0

    @classmethod
    def is_past_date(cls, deadline: DateInput, reference_date: DateInput | None = None) -> bool:
        return cls.days_difference(deadline, reference_date) < 0

    @classmethod
    def is_same_day(cls, deadline: DateInput, reference_date: DateInput | None = None) -> bool:
        return cls.days_difference(deadline, reference_date) == 0
