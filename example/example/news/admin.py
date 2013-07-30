from functools import partial

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelform_factory
from django.contrib.admin.util import flatten_fieldsets

from werewolf.admin import WerewolfBaseAdmin

from news.models import NewsItem
from news.constants import PERMISSION_CAN_CHANGE_AUTHOR, PERMISSION_CAN_CHANGE_EDITOR
from news.constants import PERMISSION_CAN_CHANGE_CHIEF_EDITOR

class NewsItemAdmin(WerewolfBaseAdmin):
    """
    News item admin.
    """
    list_display = ('title', 'date_published', 'admin_status', 'author', 'editor')
    list_filter = ('status',)
    readonly_fields = ('date_created', 'date_updated')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'teaser', 'body', 'image', 'urgency')
        }),
        (_("Workflow and Staff"), {
            'classes': ('',),
            'fields': ('author', 'editor', 'chief_editor', 'status')
        }),
        (_("Publication/expiration dates"), {
            'classes': ('',),
            'fields': ('date_published', 'expiration_date')
        }),
        (_("Event dates"), {
            'classes': ('collapse',),
            'fields': ('event_date_start', 'event_date_end')
        }),
        (_("Additional"), {
            'classes': ('collapse',),
            'fields': ('date_created', 'date_updated')
        })
    )

    class Meta:
        app_label = _('News item')

    def queryset(self, request):
        queryset = super(NewsItemAdmin, self).queryset(request)
        queryset = queryset.select_related('author', 'editor')
        return queryset

    def get_form(self, request, obj=None, **kwargs):
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

        if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_AUTHOR)):
            exclude.append('author')
        if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_EDITOR)):
            exclude.append('editor')
        if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_CHIEF_EDITOR)):
            exclude.append('chief_editor')

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
        # Hiding fields that non-authorised users should not have access to.
        fieldsets = super(NewsItemAdmin, self).get_fieldsets(request, obj=None)

        cleaned_fieldsets = []

        for fieldset_label, fieldset in fieldsets:
            fields = list(fieldset['fields'])

            # Cleaning author
            if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_AUTHOR)):
                try:
                    fields.remove('author')
                except:
                    pass

            # Cleaning editor
            if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_EDITOR)):
                try:
                    fields.remove('editor')
                except:
                    pass

            # Cleaning chief editor
            if not request.user.has_perm('%s.%s' % (NewsItem._meta.app_label, PERMISSION_CAN_CHANGE_CHIEF_EDITOR)):
                try:
                    fields.remove('chief_editor')
                except:
                    pass

            cleaned_fieldsets.append((fieldset_label, {'fields': fields}))

        return cleaned_fieldsets

admin.site.register(NewsItem, NewsItemAdmin)
