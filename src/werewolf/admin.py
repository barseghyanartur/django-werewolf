__title__ = 'werewolf.admin'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('WerewolfBaseAdmin',)

from functools import partial

from django.contrib import admin
from django import forms
from django.forms.models import modelform_factory
from django.contrib.admin.util import flatten_fieldsets

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

    :property list werewolf_protected_fields: List of fields to protect in form of the following
        tuple (``field_name``, ``required_permission``).
    """
    werewolf_protected_fields = []

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

    def get_form(self, request, obj=None, **kwargs):
        """
        Hiding fields that non-authorised users should not have access to. It's done based on the
        ``werewolf_protected_fields`` of your ``ModelAdmin``. But if happen to override that method
        for your own needs, make sure the it also reflects the django-werewolf concepts.
        """
        if not self.werewolf_protected_fields:
            return super(WerewolfBaseAdmin, self).get_form(request=request, obj=obj, **kwargs)

        # Hiding fields that non-authorised users should not have access to.
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(self.get_readonly_fields(request, obj))
        if self.exclude is None and hasattr(self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only if the
            # ModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)
        # if exclude is an empty list we pass None to be consistant with the
        # default on modelform_factory
        exclude = exclude or []

        for field_name, required_permission in self.werewolf_protected_fields:
            if not request.user.has_perm('{0}.{1}'.format(self.model._meta.app_label, required_permission)):
                exclude.append(field_name)

        exclude = exclude or None

        defaults = {
            "form": self.form,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": partial(self.formfield_for_dbfield, request=request),
        }
        defaults.update(kwargs)
        return modelform_factory(self.model, **defaults)

    def get_fieldsets(self, request, obj=None):
        """
        Hiding fields that non-authorised users should not have access to. It's done based on the
        ``werewolf_protected_fields`` of your ``ModelAdmin``. But if happen to override that method
        for your own needs, make sure the it also reflects the django-werewolf concepts.
        """
        fieldsets = super(WerewolfBaseAdmin, self).get_fieldsets(request, obj=None)
        
        if not self.werewolf_protected_fields:
            return fieldsets

        cleaned_fieldsets = []

        for fieldset_label, fieldset in fieldsets:
            fields = list(fieldset['fields'])

            for field_name, required_permission in self.werewolf_protected_fields:
                # Cleaning the field that has been already excluded from form (in ``get_form``).
                if not request.user.has_perm('{0}.{1}'.format(self.model._meta.app_label, required_permission)):
                    try:
                        fields.remove(field_name)
                    except:
                        pass

            cleaned_fieldsets.append((fieldset_label, {'fields': fields}))

        return cleaned_fieldsets
