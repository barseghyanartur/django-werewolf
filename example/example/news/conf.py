from django.conf import settings

from news import defaults

def get_setting(setting, override=None):
    """
    Get a setting from news conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'NEWS_%s' % setting):
        return getattr(settings, 'NEWS_%s' % setting)
    else:
        return getattr(defaults, setting)
