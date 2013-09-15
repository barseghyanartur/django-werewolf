from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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

    # Hiding fields that non-authorised users should not have access to.
    werewolf_protected_fields = (
        ('author', PERMISSION_CAN_CHANGE_AUTHOR),
        ('editor', PERMISSION_CAN_CHANGE_EDITOR),
        ('chief_editor', PERMISSION_CAN_CHANGE_CHIEF_EDITOR)
    )

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

admin.site.register(NewsItem, NewsItemAdmin)
