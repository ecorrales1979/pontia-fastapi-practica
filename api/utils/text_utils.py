class TextUtils:

    @staticmethod
    def _get_forbidden_words(forbidden_words: list[str] | None = None) -> list[str]:
        if forbidden_words is None:
            return [
                "tonto",
                "idiota",
                "estúpido",
            ]
        return forbidden_words

    @classmethod
    def sanitize_text(cls, text: str, forbidden_words: list[str] | None = None) -> str:
        sanitized_text = text
        for word in cls._get_forbidden_words(forbidden_words):
            if word.lower() in sanitized_text.lower():
                sanitized_text = sanitized_text.replace(word, "*" * len(word))
        return sanitized_text
