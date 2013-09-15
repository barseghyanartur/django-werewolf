__title__ = 'werewolf.triggers'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('WerewolfBaseTrigger', 'registry')

class WerewolfBaseTrigger(object):
    """
    Werewolf base trigger.
    """
    def __init__(self, obj, request):
        self.obj = obj
        self.requeset = request

    def process(self):
        raise NotImplementedError("You should define a ``process`` method in your trigger class!")


class WerewolfRegistry(object):
    """
    Trigger registry.

    Register all your werewolf triggers subclassed from ``werewolf.triggers.WerewolfBaseTrigger`` as follows:
    >>> from werewolf.triggers import WerewolfBaseTrigger, registry
    >>> 
    >>> # Our trigger
    >>> class StatusExampleTrigger(WerewolfBaseTrigger):
    >>>     def process(self):
    >>>         print 'status triggered'
    >>> 
    >>> registry.register('your-app-label', 'your-module-name', 'status-to-catch', StatusExampleTrigger)
    """
    def __init__(self):
        self._registry = {}

    def __make_key(self, app_label, module_name, status):
        return '%s.%s:%status' % (app_label, module_name, status)

    def register(self, app_label, module_name, status, trigger_class):
        """
        Registers the trigger into the global registry.

        :param str app_label:
        :param str module_name:
        :param str status:
        :param str werewolf.triggers.WerewolfBaseTrigger: Subclass of ``werewolf.triggers.WerewolfBaseTrigger``.
        """
        self._registry[self.__make_key(app_label, module_name, status)] = trigger_class

    def register_for_model(self, model, status, trigger_class):
        self._registry[self.__make_key(model._metal.app_label, model._meta.module_name, status)] = trigger_class

    def get(self, app_label, module_name, status):
        """
        Gets the trigger from global trigger registry.

        :param str app_label:
        :param str module_name:
        :param str status:
        :return werewolf.triggers.WerewolfBaseTrigger: Subclass of ``werewolf.triggers.WerewolfBaseTrigger``.
        """
        key = self.__make_key(app_label, module_name, status)
        if key in self._registry:
            return self._registry[key]

    def get_for_model(self, model, status):
        return self.get(model._meta.app_label, model._meta.module_name, status)


# Register triggers by calling registry.register()
registry = WerewolfRegistry()
