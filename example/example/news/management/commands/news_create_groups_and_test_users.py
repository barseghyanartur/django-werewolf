__version__ = '0.4'
__build__ = 0x000004
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('Command',)

from django.core.management.base import BaseCommand

from werewolf.tests import create_groups_and_test_users

from news.settings import CHIEF_EDITORS_GROUP_NAME, EDITORS_GROUP_NAME, WRITERS_GROUP_NAME

class Command(BaseCommand):
    def handle(self, *args, **options):
        create_groups_and_test_users(
            chief_editors_group_name = CHIEF_EDITORS_GROUP_NAME,
            editors_group_name = EDITORS_GROUP_NAME,
            writers_group_name = WRITERS_GROUP_NAME
            )
