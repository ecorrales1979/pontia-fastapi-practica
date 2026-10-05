from .note_mixins import ContentMixin, DeadlineMixin, TitleMixin


class NoteCreateValidator(ContentMixin, DeadlineMixin, TitleMixin):
    pass
