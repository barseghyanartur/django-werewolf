__title__ = 'werewolf.admin'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('WerewolfBaseAdmin',)

from django.contrib import admin
from django import forms

from werewolf.utils import status_choices_for_user
from werewolf.triggers import registry
from werewolf.settings import USE_DJANGO_REVERSION, DEFAULT_STATUS

if USE_DJANGO_REVERSION:
    from reversion.admin import VersionAdmin
    AdminParentClass = VersionAdmin
else:
    AdminParentClass = admin.ModelAdmin

class WerewolfBaseAdmin(AdminParentClass):
    """
    Base werewolf admin model.
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Here we replace the choices based on the user permissions.
        """
        if 'status' == db_field.name:
            status_choices = status_choices_for_user(kwargs['request'].user, self.model._meta.app_label)
            field = forms.ChoiceField(choices=status_choices, required=True, initial=DEFAULT_STATUS)
            return field

        return super(WerewolfBaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def queryset(self, request):
        """
        Make sure users with no rights to edit an object with status, don't even see it.
        """
        status_choices = dict(status_choices_for_user(request.user, self.model._meta.app_label)).keys()
        return super(WerewolfBaseAdmin, self).queryset(request).filter(status__in=status_choices)

    def status_change_trigger(self, request, obj, form, change):
        """
        Status change trigger. Executes appropriate registered trigger if applicable.

        :param django.http.HttpRequest request:
        :param django.db.models.Model obj: Subclass of ``django.db.models.Model``.
        :param form:
        :param bool change:
        """
        # It's important to perform the checks after the
        if 'status' in form.changed_data:
            Trigger = registry.get_for_model(obj, obj.status)
            if Trigger:
                trigger = Trigger(obj=obj, request=request)
                trigger.process()

    def save_model(self, request, obj, form, change):
        super(WerewolfBaseAdmin, self).save_model(request, obj, form, change)

        self.status_change_trigger(request, obj, form, change)
