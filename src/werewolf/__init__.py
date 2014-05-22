__title__ = 'werewolf.__init__'
__version__ = '0.4.3'
__build__ = 0x000006
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('autodiscover',)

import imp

def autodiscover():
    """
    Autodiscovers the werewolf triggers in project apps. Each trigger file which should be found by werewolf,
    should be named "werewolf_triggers.py".
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
        __import__('{0}.{1}'.format(app, WEREWOLF_TRIGGERS_MODULE_NAME))
