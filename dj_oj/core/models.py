import timeago
from django.db import models
from django.utils.formats import localize
from django.utils.timezone import localtime, now


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
        return self._get_relative_time('created_at')
    
    @property
    def updated_at_relative(self):
        return self._get_relative_time('updated_at')

    def _get_relative_time(self, attr):
        return timeago.format(
            getattr(self, attr),
            now(),
            'ko'
        )

    @property
    def created_at_visible(self):
        return self._get_visible_time('created_at')
    
    @property
    def updated_at_visible(self):
        return self._get_visible_time('updated_at')

    def _get_visible_time(self, attr):
        return localize(localtime(getattr(self, attr)))
