from django.db import models


class PublishedModel(models.Model):

    is_published = models.BooleanField(
        default=True, blank=False, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        blank=False, auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
