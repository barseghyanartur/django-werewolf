__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('Command',)

from django.core.management.base import BaseCommand
from django.db.models import get_models, get_app
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q

from news.settings import CHIEF_EDITORS_GROUP_NAME, EDITORS_GROUP_NAME, WRITERS_GROUP_NAME

class Command(BaseCommand):
    def handle(self, *args, **options):
        # django-reversion group name
        REVERSION_GROUP_NAME = 'Reversion'

        groups = (
            # group name, permissions
            (WRITERS_GROUP_NAME, \
             ['news.newsitem.change_newsitem', 'news.newsitem.change_status_to_new', \
              'news.newsitem.change_status_to_draft', 'news.newsitem.change_status_to_ready']),
            (EDITORS_GROUP_NAME, \
             ['news.newsitem.change_newsitem', 'news.newsitem.can_change_author', \
              'news.newsitem.change_status_to_new', 'news.newsitem.change_status_to_draft', \
              'news.newsitem.change_status_to_ready', 'news.newsitem.change_status_to_reviewed']),
            (CHIEF_EDITORS_GROUP_NAME, \
             ['news.newsitem.add_newsitem', 'news.newsitem.change_newsitem', 'news.newsitem.delete_newsitem', \
              'news.newsitem.can_change_author', 'news.newsitem.can_change_editor', \
              'news.newsitem.can_change_chief_editor', 'news.newsitem.change_status_to_new', \
              'news.newsitem.change_status_to_draft', 'news.newsitem.change_status_to_ready', \
              'news.newsitem.change_status_to_reviewed', 'news.newsitem.change_status_to_published']),
            (REVERSION_GROUP_NAME, \
             ['reversion.version.add_version', 'reversion.version.change_version', 'reversion.version.delete_version'])
        )

        for group_name, group_permissions in groups:
            try:
                # Creating the group
                group = Group()
                group.name = group_name
                group.save()

                # Adding permissions
                q = None

                for group_permission in group_permissions:
                    app_label, model, permission_name = group_permission.split('.')

                    if q is None:
                        q = Q(content_type__app_label=app_label, content_type__model=model, codename=permission_name)
                    else:
                        q = q | Q(content_type__app_label=app_label, content_type__model=model, codename=permission_name)

                permissions = Permission._default_manager.filter(q)

                group.permissions.add(*permissions)
            except Exception as e:
                pass

        users = (
            # username, password, e-mail, first name, last name
            ('admin', 'test', 'admin@example.com', 'Test Admin', 'Test Admin', []),
            ('chief_editor', 'test', 'chief-editor@example.com', 'Test Chief Editor', 'Test Chief Editor', \
             [CHIEF_EDITORS_GROUP_NAME, REVERSION_GROUP_NAME]),
            ('editor', 'test', 'editor@example.com', 'Test Editor', 'Test Editor', \
             [EDITORS_GROUP_NAME, REVERSION_GROUP_NAME]),
            ('writer', 'test', 'writer@example.com', 'Test Writer', 'Test Writer', \
             [WRITERS_GROUP_NAME, REVERSION_GROUP_NAME])
        )

        for username, password, email, first_name, last_name, groups in users:
            try:
                # Creating a new user
                user = User()
                user.username = username
                user.set_password(password)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.is_staff = True

                if 'admin' == username:
                    user.is_superuser = True

                user.save()

                # Adding created user to groups
                user_groups = Group._default_manager.filter(name__in=groups)
                user.groups.add(*user_groups)
            except Exception as e:
                pass
