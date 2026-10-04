from .note_mixins import ContentMixin, DeadlineMixin, IsDoneMixin


class NoteUpdateValidator(ContentMixin, DeadlineMixin, IsDoneMixin):
    pass
