__title__ = 'werewolf.settings'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('STATUS_CHOICES', 'STATUS_PUBLISHED', 'DEFAULT_STATUS', 'STATUS_MAX_LENGTH', 'USE_DJANGO_REVERSION')

from werewolf.conf import get_setting

STATUS_CHOICES = get_setting('STATUS_CHOICES')

STATUS_PUBLISHED = get_setting('STATUS_PUBLISHED')

DEFAULT_STATUS = get_setting('DEFAULT_STATUS')

STATUS_MAX_LENGTH = get_setting('STATUS_MAX_LENGTH')

USE_DJANGO_REVERSION = get_setting('USE_DJANGO_REVERSION')
