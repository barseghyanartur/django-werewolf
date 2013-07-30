import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from werewolf.triggers import WerewolfBaseTrigger, registry
from werewolf.helpers import admin_edit_url_for_object

from lime import send_email

from news.settings import CHIEF_EDITORS_GROUP_NAME


class StatusNewTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `new`.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            _('A new News Item has been assigned to you'),
            editor.email,
            author.email,
            {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': author.get_full_name(),
                'from_name': editor.get_full_name(),
            },
            'news/emails/new_newsitem.txt',
            'news/emails/new_newsitem.html'
        )


class StatusDraftTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `draft`.
    """
    def process(self):
        # do things here as in previous examples if needed
        pass


class StatusReadyTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `ready` (ready for review).
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            _('A News Item is ready for review!'),
            author.email,
            editor.email,
            {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': editor.get_full_name(),
                'from_name': author.get_full_name(),
            },
            'news/emails/ready_newsitem.txt',
            'news/emails/ready_newsitem.html'
        )


class StatusReviewedTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `reviewed`.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            _('A News Item has been reviewed!'),
            author.email,
            editor.email,
            {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': editor.get_full_name(),
                'from_name': author.get_full_name(),
            },
            'news/emails/reviewed_newsitem.txt',
            'news/emails/reviewed_newsitem.html'
        )


class StatusPublishedTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `published`.
    """
    def process(self):
        editor = self.obj.editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            _('A News Item has been published!'),
            [u.email for u in User._default_manager.filter(groups__name=CHIEF_EDITORS_GROUP_NAME).only('email')],
            editor.email,
            {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'front_url': self.obj.get_absolute_url(),
                'full_name': _("Chief editor"),
                'from_name': editor.get_full_name(),
            },
            'news/emails/published_newsitem.txt',
            'news/emails/published_newsitem.html'
        )


registry.register('news', 'newsitem', 'new', StatusNewTrigger)
registry.register('news', 'newsitem', 'ready', StatusReadyTrigger)
registry.register('news', 'newsitem', 'reviewed', StatusReviewedTrigger)
registry.register('news', 'newsitem', 'published', StatusPublishedTrigger)
registry.register('news', 'newsitem', 'draft', StatusDraftTrigger)
