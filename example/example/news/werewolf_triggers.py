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

    In our workflow, a Chief Editor creates an article and choses a Writer and an Editor assigned. Thus, when
    an item is created with a status new, both Author and Editor get notified. Sender is in this case the
    Chief Editor.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        chief_editor = self.obj.chief_editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            subject =_('A new News Item has been assigned to you'),
            from_email = chief_editor.email,
            to = [author.email, editor.email],
            context = {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': _("Writer/Editor"),
                'from_name': chief_editor.get_full_name(),
            },
            plain_template = 'news/emails/new_newsitem.txt',
            html_template = 'news/emails/new_newsitem.html'
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

    When Writer finishes his work on the news item, he changes its' status to `ready` and the Editor responsible
    gets a notification. Sender is the Author, recipient is the Editor.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            subject = _('A News Item is ready for review!'),
            from_email = author.email,
            to = editor.email,
            context = {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': editor.get_full_name(),
                'from_name': author.get_full_name(),
            },
            plain_template = 'news/emails/ready_newsitem.txt',
            html_template = 'news/emails/ready_newsitem.html'
        )


class StatusReviewedTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `reviewed`.

    When Editor reviews the news item written and finds it to be acceptable, he changes its' status to `reviewed`.
    The Chief Editor gets notification. Sender is the Editor, recipient is the Chief Editor.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        chief_editor = self.obj.chief_editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            subject = _('A News Item has been reviewed!'),
            from_email = editor.email,
            to = chief_editor.email,
            context = {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'full_name': chief_editor.get_full_name(),
                'from_name': editor.get_full_name(),
            },
            plain_template = 'news/emails/reviewed_newsitem.txt',
            html_template = 'news/emails/reviewed_newsitem.html'
        )


class StatusPublishedTrigger(WerewolfBaseTrigger):
    """
    News item status changed to `published`.

    A news items is published. All Chief Editors get notified about it. Author and Editor get notification via
    BCC.
    """
    def process(self):
        author = self.obj.author
        editor = self.obj.editor
        chief_editor = self.obj.chief_editor
        edit_url = admin_edit_url_for_object(self.obj)
        send_email(
            subject = _('A News Item has been published!'),
            from_email = editor.email,
            to = [u.email for u in User._default_manager.filter(groups__name=CHIEF_EDITORS_GROUP_NAME).only('email')],
            context = {
                'date_submitted': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'url': edit_url,
                'front_url': self.obj.get_absolute_url(),
                'full_name': _("Team"),
                'from_name': chief_editor.get_full_name(),
            },
            plain_template = 'news/emails/published_newsitem.txt',
            html_template = 'news/emails/published_newsitem.html',
            bcc = [author.email, editor.email]
        )


registry.register('news', 'newsitem', 'new', StatusNewTrigger)
registry.register('news', 'newsitem', 'ready', StatusReadyTrigger)
registry.register('news', 'newsitem', 'reviewed', StatusReviewedTrigger)
registry.register('news', 'newsitem', 'published', StatusPublishedTrigger)
registry.register('news', 'newsitem', 'draft', StatusDraftTrigger)
