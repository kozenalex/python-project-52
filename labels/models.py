from django.db import models
from django.utils.translation import gettext as _


class Labels(models.Model):

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
