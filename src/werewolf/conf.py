from django.conf import settings

from werewolf import defaults

def get_setting(setting, override=None):
    """
    Get a setting from `werewolf` conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'WEREWOLF_%s' % setting):
        return getattr(settings, 'WEREWOLF_%s' % setting)
    else:
        return getattr(defaults, setting)
