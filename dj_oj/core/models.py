import timeago
from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='생성일',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='수정일',
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    @property
    def created_at_relative(self):
        return timeago.format(
            self.created_at,
            now(),
            'ko',
        )
