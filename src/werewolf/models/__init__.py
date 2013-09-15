__title__ = 'werewolf.models.__init__'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('WerewolfBaseMeta', 'WerewolfBaseModel')

from django.db import models
from django.utils.translation import ugettext_lazy as _

from werewolf.models.managers import WerewolfBaseManager
from werewolf.utils import extend_werewolf_permissions
from werewolf.conf import get_setting

STATUS_CHOICES = get_setting('STATUS_CHOICES')
DEFAULT_STATUS = get_setting('DEFAULT_STATUS')
STATUS_MAX_LENGTH = get_setting('STATUS_MAX_LENGTH')

class WerewolfBaseMeta(object):
    """
    Base Meta class of the ``WerewolfBaseModel``. Every subclass of the ``WerewolfBaseModel``
    shall extend it:
    
    >>> from werewolf.models import WerewolfBaseModel, WerewolfBaseMeta
    >>> class NewsItem(WerewolfBaseModel): # Important!
    >>>     # Your fields here
    >>>     class Meta(WerewolfBaseMeta): # Important!
    >>>         verbose_name = "News item"
    >>>         verbose_name_plural = "News items"

    Alternatively you can add the ``permissions`` attribute:

    >>> from werewolf.utils import extend_werewolf_permissions
    >>> class NewsItem(WerewolfBaseModel):
    >>>     # Your fields here
    >>>     class Meta:
    >>>         verbose_name = "News item"
    >>>         verbose_name_plural = "News items"
    >>>         permissions = extend_werewolf_permissions(
    >>>             ('can_change_author', _("Can change author")),
    >>>             ('can_change_editor', _("Can change editor")),
    >>>         )
    """
    permissions = extend_werewolf_permissions()


class WerewolfBaseModel(models.Model):
    """
    Base Werewolf model. If you want to have a workflow in your model (for statuses like new, draft, 
    published, etc) you should extend this model.
    """
    status = models.CharField(_("Status"), max_length=STATUS_MAX_LENGTH, choices=STATUS_CHOICES, \
                              default=DEFAULT_STATUS)

    objects = WerewolfBaseManager()

    class Meta(WerewolfBaseMeta):
        abstract = True
