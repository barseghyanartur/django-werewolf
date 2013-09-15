__title__ = 'werewolf.defaults'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('STATUS_CHOICES', 'STATUS_PUBLISHED', 'DEFAULT_STATUS', 'STATUS_MAX_LENGTH', 'USE_DJANGO_REVERSION')

gettext = lambda s: s

# Status choices for the workflow. When customizing pay extra attention to `STATUS_PUBLISHED` and `DEFAULT_STATUS`
# as they should match those set in `STATUS_CHOICES`. Order is preserved.
STATUS_CHOICES = (
    ('new', gettext('New')), # New - this is how it's assigned to a writer.
    ('draft', gettext('Draft')), # Draft - this is how the writer works on it.
    ('ready', gettext('Ready')), # Ready to be reviewed by editor.
    ('reviewed', gettext('Reviewed')), # Reviewed by editor (means positive and ready to be published).
    ('published', gettext('Published')), # Published.
)

# Published status.
STATUS_PUBLISHED = 'published'

# Default status. Be careful with this. All users must have permissions to this status. Otherwise, set to None.
DEFAULT_STATUS = None

# It's unlikely that you're going to exceed the 50 chars limit for the status. Still, possible to customise.
STATUS_MAX_LENGTH = 50

# When set to True, django-reversion is used.
USE_DJANGO_REVERSION = True
