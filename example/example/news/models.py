import datetime
from pytz import timezone

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from werewolf.models import WerewolfBaseModel
from werewolf.utils import extend_werewolf_permissions

from news.constants import PERMISSION_CAN_CHANGE_AUTHOR, PERMISSION_CAN_CHANGE_EDITOR
from news.constants import PERMISSION_CAN_CHANGE_CHIEF_EDITOR

NEWS_IMAGES_STORAGE_PATH = 'news-images'


def _news_images(instance, filename):
    """
    Store the images in their own folder. This allows us to keep thumbnailed versions of all images.
    """
    if instance.pk:
        return '%s/%s-%s' % (NEWS_IMAGES_STORAGE_PATH, str(instance.pk), filename.replace(' ', '-'))
    return '%s/%s' % (NEWS_IMAGES_STORAGE_PATH, filename.replace(' ', '-'))


_chief_editors = {'groups__name__iexact': 'Chief editors'}
_editors = {'groups__name__iexact': 'Editors'}
_writers = {'groups__name__iexact': 'Writers'}


class NewsItem(WerewolfBaseModel):
    """
    News item.

    ``title`` Title of the news item.
    ``teaser`` Teaser of the news item. Plain text.
    ``body`` Teaser of the news item. WYSIWYG.
    ``author`` Author of the news item.
    ``editor`` Editor of the news item.
    ``chief_editor`` Chief editor of the news item.
    ``image`` Headline image of the news item.
    ``urgency`` Urgency of the news item.
    ``date_published`` Date item is published. On creating defaults to ``datetime.datetime.now``.
    ``event_date_start`` Event start date.
    ``event_date_end`` Event end date.
    ``expiration_date`` Expiration date. After that date the article expires and is no longer shown.
    """
    # Urgency statuses
    URGENCY_STATUS_NORMAL = 'nrm'
    URGENCY_STATUS_URGENT = 'urg'
    URGENCY_STATUSES = (
        (URGENCY_STATUS_URGENT, _("Urgent")),
        (URGENCY_STATUS_NORMAL, _("Not urgent")),
    )
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(_("Slug"), blank=False, null=False, unique=True)
    teaser = models.TextField(_("Teaser"), blank=True, null=True)
    body = models.TextField(_("Body"))
    author = models.ForeignKey(User, verbose_name=_("Author"), related_name='authors', limit_choices_to=_writers)
    editor = models.ForeignKey(User, verbose_name=_("Editor"), related_name='editors', limit_choices_to=_editors)
    chief_editor = models.ForeignKey(User, verbose_name=_("Chief editor"), related_name='chief_editors', \
                                     limit_choices_to=_chief_editors)
    image = models.ImageField(_("Headline image"), blank=True, null=True, upload_to=_news_images)
    urgency = models.CharField(_("Urgency"), max_length=10, blank=True, null=True, choices=URGENCY_STATUSES)
    date_published = models.DateTimeField(_("Date published"), default=datetime.datetime.now())
    expiration_date = models.DateTimeField(_("Expiration date"), blank=True, null=True)
    event_date_start = models.DateTimeField(_("Event date start"), blank=True, null=True, \
                                            help_text=_("Should be filled together with `event end date`."))
    event_date_end = models.DateTimeField(_("Event date end"), blank=True, null=True, \
                                            help_text=_("Should be filled together with `event end date`."))

    date_created = models.DateTimeField(_("Date created"), blank=True, null=True, auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("Date updated"), blank=True, null=True, auto_now=True, editable=False)

    class Meta:
        verbose_name = _("News item")
        verbose_name_plural = _("News items")

        permissions = extend_werewolf_permissions(
            (PERMISSION_CAN_CHANGE_AUTHOR, _("Can change author")),
            (PERMISSION_CAN_CHANGE_EDITOR, _("Can change editor")),
            (PERMISSION_CAN_CHANGE_CHIEF_EDITOR, _("Can change chief editor"))
        )

    def __unicode__(self):
        return self.title

    def clean(self):
        """
        Validation happens here.
        """
        if self.event_date_start or self.event_date_end:
            if not (self.event_date_start and self.event_date_end):
                raise ValidationError(_("When given, both `Event start date` and `Event end date` shall be filled in."))
            if self.event_date_start > self.event_date_end:
                raise ValidationError(_("`Event start date` can't come later than `Event end date`."))

    def is_expired(self):
        """
        Check if news item is expired.

        :return bool:
        """
        if not self.expiration_date:
            return False

        now = datetime.datetime.now()
        local_zone = timezone(settings.TIME_ZONE)
        local_now = local_zone.localize(now)

        if self.expiration_date > local_now:
            return False

        return True

    def admin_status(self):
        """
        Adds app specific status `Expired` to expired published articles. For admin use mainly.

        :return str:
        """
        if self.is_expired():
            return _("expired")

        return self.status
    admin_status.allow_tags = True
    admin_status.short_description = _('Status')
