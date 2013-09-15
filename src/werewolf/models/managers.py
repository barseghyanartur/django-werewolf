__title__ = 'werewolf.models.managers'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('WerewolfBaseManager',)

from django.db import models

from werewolf.settings import STATUS_PUBLISHED

class WerewolfBaseManager(models.Manager):
    """
    Werewolf base manager.
    """
    def published(self):
        return self.filter(status__exact=STATUS_PUBLISHED)
