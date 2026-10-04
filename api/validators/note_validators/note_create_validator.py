from .note_mixins import ContentMixin, DeadlineMixin


class NoteCreateValidator(ContentMixin, DeadlineMixin):
    pass
