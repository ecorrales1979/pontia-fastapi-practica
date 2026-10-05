from .note_mixins import ContentMixin, DeadlineMixin, IsDoneMixin, TitleMixin


class NoteUpdateValidator(ContentMixin, DeadlineMixin, IsDoneMixin, TitleMixin):
    pass
