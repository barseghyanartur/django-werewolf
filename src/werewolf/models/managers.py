__all__ = ('WerewolfBaseManager',)

from django.db import models

from werewolf.settings import STATUS_PUBLISHED


class WerewolfBaseManager(models.Manager):
    """
    Werewolf base manager.
    """
    def published(self):
        return self.filter(status__exact=STATUS_PUBLISHED)
