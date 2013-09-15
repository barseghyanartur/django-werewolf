__title__ = 'werewolf.views'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('autodiscover',)

import imp

from django.conf import settings

def autodiscover():
    """
    Autodiscovers the werewolf in project apps. Each report file which should be found by werewolf, should be
    named "werewolf_triggers.py".
    """
    from django.conf import settings

    WEREWOLF_TRIGGERS_MODULE_NAME = 'werewolf_triggers'

    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        try:
            imp.find_module(WEREWOLF_TRIGGERS_MODULE_NAME, app_path)
        except ImportError:
            continue
        __import__('%s.%s' % (app, WEREWOLF_TRIGGERS_MODULE_NAME))
