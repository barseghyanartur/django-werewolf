__title__ = 'werewolf.models.managers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('WerewolfBaseManager',)

from django.db import models

from werewolf.settings import STATUS_PUBLISHED

class WerewolfBaseManager(models.Manager):
    """
    Werewolf base manager.
    """
    def published(self):
        return self.filter(status__exact=STATUS_PUBLISHED)
