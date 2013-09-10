Package
==================================
django-werewolf

Description
==================================
Item publishing workflow for Django (fully integrated into Django admin).

Prerequisites
===================================
- Django 1.5.+
- Python 2.7.+, 3.3.+

Installation
==================================
1. Install django-werewolf into your virtual environment:

    $ pip install django-werewolf

2. Add `werewolf` to your ``INSTALLED_APPS``.

That's all. See the `Usage and examples` section for more.

Usage and examples
==================================
It's all about item publishing in a workflow. We have various `intermediate` statuses (work in-progress) and a
final `status` which means that the item is actually published. Some users should be able to set the item status
to `published`, some others not. This app allows you (and gives you a good working example with pre-configured
Django environment) to write a custom workflow for publishing your items with minimal efforts.

For a complete example of a working django-werewolf app see the
(https://github.com/barseghyanartur/django-werewolf/tree/stable/example) and read the `readme.rst` of the `news`
app.

settings.py
----------------------------------
>>> # Workflow statuses; order is preserved.
>>> WEREWOLF_STATUS_CHOICES = (
>>>     ('new', gettext('New')), # New - this is how it's assigned to a writer.
>>>     ('draft', gettext('Draft')), # Draft - this is how the writer works on it.
>>>     ('ready', gettext('Ready')), # Ready to be reviewed by editor.
>>>     ('reviewed', gettext('Reviewed')), # Reviewed by editor (means positive and ready to be published).
>>>     ('published', gettext('Published')), # Published.
>>> )
>>>
>>> # Published status.
>>> WEREWOLF_STATUS_PUBLISHED = 'published'
>>>
>>> # When set to True, django-reversion is used.
>>> WEREWOLF_USE_DJANGO_REVERSION = True

news/models.py
----------------------------------
In the example below we have a basic news item model. We have Chief Editors with full access to news items, we
have editors with less privelleges and Writers with very little privelleges. Chief Editors create articles,
select an Editor and a Writer (both get notified) and let them work on the article. Writers can only set an
article status to `new`, `draft` and `ready` (ready to be checked). Editors review the articles with status
`ready` and set the status to `reviewed`. Chief Editors publish articles that are `reviewed`. Your
implementation can be as custom as you want it. Think in Django user groups (``django.contrib.auth.models.Group``)
and Django permissions system.

NOTE: See the `Permission tuning` section.

>>> from django.contrib.auth.models import User
>>>
>>> from werewolf.models import WerewolfBaseModel, WerewolfBaseMeta
>>>
>>> _chief_editors = {'groups__name__iexact': 'Chief editors'}
>>> _editors = {'groups__name__iexact': 'Editors'}
>>> _writers = {'groups__name__iexact': 'Writers'}
>>>
>>> class NewsItem(WerewolfBaseModel): # Important!
>>>     title = models.CharField(_("Title"), max_length=100)
>>>     body = models.TextField(_("Body"))
>>>     date_published = models.DateTimeField(_("Date published"), \
>>>                                           default=datetime.datetime.now())
>>>     author = models.ForeignKey(User, verbose_name=_("Author"), related_name='authors', \
>>>                                limit_choices_to=_writers)
>>>     editor = models.ForeignKey(User, verbose_name=_("Editor"), related_name='editors', \
>>>                                limit_choices_to=_editors)
>>>     chief_editor = models.ForeignKey(User, verbose_name=_("Chief editor"), \
>>>                                      related_name='chief_editors', \
>>>                                      limit_choices_to=_chief_editors)
>>>
>>>     class Meta(WerewolfBaseMeta): # Important!
>>>         verbose_name = "News item"
>>>         verbose_name_plural = "News items"

Or if you want to define custom permissions for your model as well, do extend the werewolf permissions as
follows:

>>> from werewolf.models import WerewolfBaseModel
>>> from werewolf.utils import extend_werewolf_permissions
>>>
>>> class NewsItem(WerewolfBaseModel):
>>>     # Your fields here
>>>     class Meta:
>>>         verbose_name = "News item"
>>>         verbose_name_plural = "News items"
>>>
>>>         # Important!
>>>         permissions = extend_werewolf_permissions(
>>>             ('can_change_author', _("Can change author")),
>>>             ('can_change_editor', _("Can change editor")),
>>>             ('can_change_chief_editor', _("Can change chief editor"))
>>>         )

news/admin.py
----------------------------------
Basic admin for the news item model.

NOTE: See the `Permission tuning` section.

>>> from werewolf.admin import WerewolfBaseAdmin
>>>
>>> from news.models import NewsItem
>>>
>>> class NewsItemAdmin(WerewolfBaseAdmin):
>>>     # Your code comes here
>>>
>>> admin.site.register(NewsItem, NewsItemAdmin)

NOTE: If you override the ``queryset`` method of your model's admin class, make sure to see the source code
of `werewolf.admin.WerewolfBaseAdmin.queryset` and copy the approach from there. Otherwise, your users with
no permission to change the `published` status will be able to chgange the status of already published items
to non-published statuses.

news/views.py
----------------------------------
>>> from news.models import NewsItem
>>>
>>> def browse(request):
>>>     news_items = NewsItem._default_manager.published()
>>>     # Other code

news/werewolf_triggers.py
----------------------------------
In order to perform extra tasks on status change, triggers are used. You simply make a new file in your app
called `werewolf_triggers.py` and define custom classes that should be called when a ``status`` field of your
model changes to a certain value. Each trigger should subclass the ``werewolf.triggers.WerewolfBaseTrigger``
class.

>>> from werewolf.triggers import WerewolfBaseTrigger, registry
>>>
>>> class StatusNewTrigger(WerewolfBaseTrigger):
>>>     """
>>>     News item status changed to `new`.
>>>     """
>>>     def process(self):
>>>         # Your code
>>>
>>> class StatusReadyTrigger(WerewolfBaseTrigger):
>>>     """
>>>     News item status changed to `ready` (ready for review).
>>>     """
>>>     def process(self):
>>>         # Your code
>>>
>>> # Triggers status change to `new` for news.newsitem model.
>>> registry.register('news', 'newsitem', 'new', StatusNewTrigger)
>>>
>>> # Triggers status change to `ready` for news.newsitem model.
>>> registry.register('news', 'newsitem', 'ready', StatusReadyTrigger)

urls.py
----------------------------------
In order to have triggers autodiscovered, place the following code into your main `urls` module.

>>> from werewolf import autodiscover as werewolf_autodiscover
>>> werewolf_autodiscover()

Permission tuning
----------------------------------
Have in mind our ``news.models.NewsItem`` model.

1. Create three user groups:

    a.  Chief editors (permissions listed):

    - news | News item | Can add News item
    - news | News item | Can change author
    - news | News item | Can change chief editor
    - news | News item | Can change editor
    - news | News item | Can change News item
    - news | News item | Can change status to draft
    - news | News item | Can change status to new
    - news | News item | Can change status to published
    - news | News item | Can change status to ready
    - news | News item | Can change status to reviewed
    - news | News item | Can delete News item

    b. Editors (permissions listed):

    - news | News item | Can change News item
    - news | News item | Can change author
    - news | News item | Can change status to draft
    - news | News item | Can change status to new
    - news | News item | Can change status to ready
    - news | News item | Can change status to reviewed

    c. Writers (permissions listed):

    - news | News item | Can change News item
    - news | News item | Can change status to draft
    - news | News item | Can change status to new
    - news | News item | Can change status to ready

3. Create three users:

    - chief editor: Belongs to group `Chief editors`.
    - editor: Belongs to group `Editors`.
    - writer: Belongs to group `Writers`.

4. Now log into the admin with different user and see your admin for the `News item` (created items with 
   `chiefeditor` account, then view them with `editor` and `writer`.

That's it. If somehow you don't see the new permissions (`Can change status to draft`,
`Can change status to new`, etc) run a management command `syncww`:

    $ ./manage.py syncww

Running the example project
==================================
A working example of a django-werewolf app is available here:
https://github.com/barseghyanartur/django-werewolf/tree/stable/example

1. Go to example/example directory

    $ cd example/example

2. Install requirements (in your virtual environment)

    $ pip install -r ../requirements.txt

3. Copy local_settings.example to local_settings.py

    $ cp local_settings.example local_settings.py

4. Create the database

    $ ./manage.py syncdb

5. Run the project

    $ ./manage.py runserver

License
==================================
GPL 2.0/LGPL 2.1

Support
==================================
For any issues contact me at the e-mail given in the `Author` section.

Author
==================================
Artur Barseghyan <artur.barseghyan@gmail.com>