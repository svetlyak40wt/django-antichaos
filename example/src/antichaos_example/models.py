from django.utils.translation import ugettext_lazy as _
from django.db import models

from tagging.fields import TagField

__all__ = ['Link']

class Link(models.Model):
    url = models.URLField(_('URL'), verify_exists = False)
    tags = tags = TagField()

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ('url',)
