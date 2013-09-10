__title__ = 'werewolf.utils'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('permission_key', 'permissions_for_base_model', 'status_choices_for_user', \
           'extend_werewolf_permissions')

from django.utils.translation import ugettext_lazy as _

from werewolf.settings import STATUS_CHOICES
from werewolf.constants import CHANGE_STATUS_TO #, CAN_VIEW_STATUS

CHOICES = dict(STATUS_CHOICES)

CHOICES_KEYS = [choice[0] for choice in STATUS_CHOICES]

def permission_key(status, choice_key):
    """
    Gets the permission key from ``choice_key`` given.

    :param str status:
    :param str choice_key:
    :return str:
    """
    return '%s_%s' % (status, choice_key)

def permissions_for_base_model(permissions=[]):
    """
    Gets/extends permissions for the base model based on the ``STATUS_CHOICES`` defined.

    :param list|tuple permissions: Permissions you want to have in your model. Those permissions would be
        extended by werewolf permissions.
    :return list:
    """
    werewolf_permissions = []
    for choice_key in CHOICES_KEYS:
        werewolf_permissions.append(
            (permission_key(CHANGE_STATUS_TO, choice_key), _("Can change status to %s") % choice_key)
            )
        # Not sure if this shall be taken out. This allows viewsing the status. Leave out for now.
        #permissions.append((permission_key(CAN_VIEW_STATUS, choice_key), _("Can view status %s") % choice_key))

    if isinstance(permissions, list):
        werewolf_permissions.extend(permissions)
    elif isinstance(permissions, tuple):
        permissions = list(permissions)
        werewolf_permissions.extend(permissions)

    return werewolf_permissions

def extend_werewolf_permissions(*args):
    """
    Extends model permissions with werewolf permissions.

    :example:
    >>> from werewolf.models import WerewolfBaseModel
    >>> from werewolf.utils import extend_werewolf_permissions
    >>> class NewsItem(WerewolfBaseModel):
    >>>     # Some fields here
    >>>
    >>>     class Meta:
    >>>         verbose_name = _("News item")
    >>>         verbose_name_plural = _("News items")
    >>>
    >>>         permissions = extend_werewolf_permissions(
    >>>             ('can_change_author', _("Can change author")),
    >>>             ('can_change_editor', _("Can change editor")),
    >>>             ('can_change_chief_editor', _("Can change chief editor"))
    >>>         )
    """
    return permissions_for_base_model(args)

def status_choices_for_user(user, app_label):
    """
    Gets available status choices for the user given.

    :param django.contrib.auth.models.User user: User for who the permissions are checked.
    :param str module_name: `app_label` of the model to check permissions to.
    :return list: List of choices in a same form as ``werewolf.defaults.STATUS_CHOICES`` but then limited
        to actual choices that user has permissions to.
    """
    statuses = []
    for choice_key in CHOICES_KEYS:
        if user.has_perm('%s.%s' % (app_label, permission_key(CHANGE_STATUS_TO, choice_key))):
            statuses.append((choice_key, CHOICES[choice_key]))

    return statuses
