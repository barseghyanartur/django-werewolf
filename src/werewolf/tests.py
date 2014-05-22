from __future__ import print_function

__title__ = 'werewolf.tests'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import unittest
import os

import random

from six import PY3

if PY3:
    from string import punctuation
else:
    from string import translate, maketrans, punctuation

from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from werewolf.settings import STATUS_CHOICES

PROJECT_DIR = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

PRINT_INFO = True

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        print('\n\n%s' % func.__name__)
        print('============================')
        if func.__doc__:
            print('""" %s """' % func.__doc__.strip())
        print('----------------------------')
        if result is not None:
            print(result)
        print('\n++++++++++++++++++++++++++++')

        return result
    return inner

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

FACTORY = """
    Sed dictum in tellus non iaculis. Aenean ac interdum ipsum. Etiam tempor quis ante vel rhoncus. Nulla
    facilisi. Curabitur iaculis consequat odio ut imperdiet? Integer accumsan; nisl vitae fermentum malesuada,
    sapien nulla sodales orci, et elementum lacus purus vel purus! Nullam orci neque, tristique in porta id,
    pretium ac sem. Fusce non est risus. Fusce convallis tellus augue, quis volutpat tellus dapibus sagittis.
    Integer lacinia commodo risus vel cursus. Etiam vitae dui in dolor porta luctus sed id elit. Nulla et est
    nec magna facilisis sagittis. Praesent tincidunt dictum lectus, sed aliquam eros. Donec placerat tortor ut
    lorem facilisis congue. Quisque ac risus nibh. Etiam ultrices nibh justo; sed mollis ipsum dapibus vitae.Ut
    vitae molestie erat. Mauris ac justo quis ante posuere vehicula. Vivamus accumsan mi volutpat diam lacinia,
    vitae semper lectus pharetra. Cras ultrices arcu nec viverra consectetur. Cras placerat ante quis dui
    consequat cursus. Nulla at enim dictum, consectetur ligula eget, vehicula nisi. Suspendisse eu ligula vitae
    est tristique accumsan nec adipiscing risus.Donec tempus dui eget mollis fringilla. Fusce eleifend lacus lectus,
    vel ornare felis lacinia ut. Morbi vel adipiscing augue. Vestibulum ante ipsum primis in faucibus orci luctus et
    ultrices posuere cubilia Curae; Cras mattis pulvinar lacus, vitae pulvinar magna egestas non. Aliquam in urna
    quis leo feugiat faucibus. Aliquam erat volutpat. Maecenas non mauris libero. Suspendisse nisi lorem, cursus a
    tristique a, porttitor in nisl. Mauris pellentesque gravida mi non mattis. Cras mauris ligula, interdum semper
    tincidunt sed, ornare a ipsum. Nulla ultrices tempus tortor vitae vehicula.Etiam at augue suscipit, vehicula
    sapien sit amet; eleifend orci. Etiam venenatis leo nec cursus mattis. Nulla suscipit nec lorem et lobortis.
    Donec interdum vehicula massa sed aliquam. Praesent eleifend mi sed mi pretium pellentesque. In in nisi tincidunt,
    commodo lorem quis; tincidunt nisl. In suscipit quam a vehicula tincidunt! Fusce vitae varius nunc. Proin at
    ipsum ac tellus hendrerit ultricies. Phasellus auctor hendrerit sapien viverra facilisis. Suspendisse lacus erat,
    cursus at dolor in, vulputate convallis sapien. Etiam augue nunc, lobortis vel viverra sit amet, pretium et
    lacus.Pellentesque elementum lectus eget massa tempus elementum? Nulla nec auctor dolor. Aliquam congue purus
    quis libero fermentum cursus. Etiam quis massa ac nisl accumsan convallis vitae ac augue. Mauris neque est,
    posuere quis dolor non, volutpat gravida tortor. Cum sociis natoque penatibus et magnis dis parturient montes,
    nascetur ridiculus mus. Vivamus ullamcorper, urna at ultrices aliquam, orci libero gravida ligula, non pulvinar
    sem magna sed tortor. Sed elementum leo viverra ipsum aliquet convallis. Suspendisse scelerisque auctor sapien.
    Mauris enim nisl, sollicitudin at rhoncus vitae, convallis nec mauris. Phasellus sollicitudin dui ut luctus
    consectetur. Vivamus placerat, neque id sagittis porttitor, nunc quam varius dolor, sit amet egestas nulla
    risus eu odio. Mauris gravida eleifend laoreet. Aenean a nulla nisl. Integer pharetra magna adipiscing, imperdiet
    augue ac, blandit felis. Cras id aliquam neque, vel consequat sapien.Duis eget vulputate ligula. Aliquam ornare
    dui non nunc laoreet, non viverra dolor semper. Aenean ullamcorper velit sit amet dignissim fermentum! Aenean urna
    leo, rutrum volutpat mauris nec, facilisis molestie tortor. In convallis pellentesque lorem, a lobortis erat
    molestie et! Ut sed sem a odio aliquam elementum. Morbi pretium velit libero, adipiscing consequat leo dignissim
    eu. Mauris vestibulum feugiat risus; quis pharetra purus tincidunt quis. Morbi semper tincidunt lorem id iaculis.
    Quisque non pulvinar magna. Morbi consequat eleifend neque et iaculis. Fusce non laoreet urna. Donec ut nunc
    ultrices, fringilla nunc ut, tempor elit. Phasellus semper sapien augue, in gravida neque egestas at.
    Integer dapibus lacus vitae luctus sagittis! Suspendisse imperdiet tortor eget mattis consectetur. Aliquam viverra
    purus a quam lacinia euismod. Nunc non consequat mi; ac vehicula lacus. Pellentesque accumsan ac diam in fermentum!
    Maecenas quis nibh sed dolor adipiscing facilisis. Aenean vel arcu eu est fermentum egestas vulputate eget purus.
    Sed fermentum rhoncus dapibus. Quisque molestie magna eu accumsan lobortis. Vestibulum cursus euismod posuere.
    Aliquam eu dapibus urna. Nulla id accumsan justo. Vivamus vitae ullamcorper tellus. Class aptent taciti sociosqu
    ad litora torquent per conubia nostra, per inceptos himenaeos.Donec pulvinar tempus lectus vitae ultricies.
    Vestibulum sagittis orci quis risus ultricies feugiat. Nunc feugiat velit est, at aliquam massa tristique eu.
    Aenean quis enim vel leo vestibulum volutpat in non elit. Quisque molestie tincidunt purus; ac lacinia mauris
    rhoncus in. Nullam id arcu at mauris varius viverra ut vitae massa. In ac nunc ipsum. Proin consectetur urna sit
    amet mattis vulputate. Nullam lacinia pretium tempus. Aenean quis ornare metus, tempus volutpat neque. Mauris
    volutpat scelerisque augue; at lobortis nulla rhoncus vitae. Mauris at lobortis turpis. Vivamus et ultrices lacus.
    Donec fermentum neque in eros cursus, ac tincidunt sapien consequat. Curabitur varius commodo rutrum. Nulla
    facilisi. Ut feugiat dui nec turpis sodales aliquam. Quisque auctor vestibulum condimentum. Quisque nec eros
    lorem. Curabitur et felis nec diam dictum ultrices vestibulum ac eros! Quisque eu pretium lacus. Morbi bibendum
    sagittis rutrum. Nam eget tellus quam. Nullam pharetra vestibulum justo. Donec molestie urna et scelerisque
    laoreet? Sed consectetur pretium hendrerit. Quisque erat nulla, elementum sit amet nibh vel, posuere pulvinar
    nulla. Donec elementum adipiscing dictum! Nam euismod semper nisi, eu lacinia felis placerat vel! Praesent eget
    dapibus turpis, et fringilla elit. Maecenas quis nunc cursus felis fringilla consequat! Cum sociis natoque
    penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed ullamcorper libero quis nisl sollicitudin,
    ut pulvinar arcu consectetur. Donec nisi nibh, condimentum et lectus non, accumsan imperdiet ipsum. Maecenas vitae
    massa eget lorem ornare dignissim. Nullam condimentum mauris id quam tincidunt venenatis. Aenean mattis viverra
    sem, vitae luctus velit rhoncus non. Vestibulum leo justo, rhoncus at aliquam et, iaculis sed dolor. Integer
    bibendum vitae urna in ornare! Cras accumsan nulla eu libero tempus, in dignissim augue imperdiet. Vivamus a
    lacinia odio. Curabitur id egestas eros. Integer non rutrum est. In nibh sem, tempus ac dignissim vel, ornare ac
    mi. Nulla congue scelerisque est nec commodo. Phasellus turpis lorem, sodales quis sem id, facilisis commodo
    massa. Vestibulum ultrices dolor eget purus semper euismod? Fusce id congue leo. Quisque dui magna, ullamcorper
    et leo eget, commodo facilisis ipsum. Curabitur congue vitae risus nec posuere. Phasellus tempor ligula in nisl
    pellentesque mattis. Sed nunc turpis, pharetra vel leo ac, lacinia cursus risus. Quisque congue aliquet volutpat.
    Integer dictum est quis semper tristique. Donec feugiat vestibulum tortor, id fringilla nisi lobortis eu. Nam
    hendrerit egestas sem, non mollis tortor iaculis quis. Phasellus id aliquet erat. Nunc facilisis nisi dolor,
    quis semper dui euismod vel. Cras convallis bibendum tortor malesuada tincidunt. Sed urna quam, pellentesque
    eget eleifend ac, consequat bibendum urna. Sed fringilla elit hendrerit leo blandit laoreet eget quis quam!
    Morbi eu leo a dolor aliquet dictum. Suspendisse condimentum mauris non ipsum rhoncus, sit amet hendrerit augue
    gravida. Quisque facilisis pharetra felis faucibus gravida. In arcu neque, gravida ut fermentum ut, placerat eu
    quam. Nullam aliquet lectus mauris, quis dignissim est mollis sed. Ut vestibulum laoreet eros quis cursus. Proin
    commodo eros in mollis mollis. Mauris bibendum cursus nibh, sit amet eleifend mauris luctus vitae. Sed aliquet
    pretium tristique. Morbi ultricies augue a lacinia porta. Nullam mollis erat non imperdiet imperdiet. Etiam
    tincidunt fringilla ligula, in adipiscing libero viverra eu. Nunc gravida hendrerit massa, in pellentesque nunc
    dictum id.
    """

if PY3:
    split_words = lambda f: list(set(f.lower().translate(str.maketrans("", "", punctuation)).split()))
else:
    split_words = lambda f: list(set(translate(f.lower(), maketrans(punctuation, ' ' * len(punctuation))).split()))

split_sentences = lambda f: f.split('?')
change_date = lambda: bool(random.randint(0, 1))

WORDS = split_words(FACTORY)
SENTENCES = split_sentences(FACTORY)
NUM_ITEMS = 50

_ = lambda s: s

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def create_groups_and_test_users(chief_editors_group_name, editors_group_name, writers_group_name):
    # django-reversion group name
    REVERSION_GROUP_NAME = 'Reversion'

    groups = (
        # group name, permissions
        (writers_group_name, \
         ['news.newsitem.change_newsitem', 'news.newsitem.change_status_to_new', \
          'news.newsitem.change_status_to_draft', 'news.newsitem.change_status_to_ready']),
        (editors_group_name, \
         ['news.newsitem.change_newsitem', 'news.newsitem.can_change_author', \
          'news.newsitem.change_status_to_new', 'news.newsitem.change_status_to_draft', \
          'news.newsitem.change_status_to_ready', 'news.newsitem.change_status_to_reviewed']),
        (chief_editors_group_name, \
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
         [chief_editors_group_name, REVERSION_GROUP_NAME]),
        ('editor', 'test', 'editor@example.com', 'Test Editor', 'Test Editor', \
         [editors_group_name, REVERSION_GROUP_NAME]),
        ('writer', 'test', 'writer@example.com', 'Test Writer', 'Test Writer', \
         [writers_group_name, REVERSION_GROUP_NAME])
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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CHIEF_EDITORS_GROUP_NAME = 'Chief editors'

EDITORS_GROUP_NAME = 'Editors'

WRITERS_GROUP_NAME = 'Writers'

class WerewolfTest(LiveServerTestCase): #unittest.TestCase
    """
    Tests of ``werewolf`` package. Since `django-werewolf` is does not have
    own views, but serves rather as a helper to build item publishing workflow.

    - Chief Editor creates a News item and chooses a Writer and an Editor. The status of a new News item is
      then set to `new`.
    - Once a News item with status `new` has been created, both Writer and the Editor assigned do get an e-mail
      notification about the fact that a News item has been assigned to them.
    - Writer is supposed to fill the assigned News item with content and once the News item is ready, change
      its' status to `ready`.
    - The assigned Editor would get an e-mail notification about the fact that the News item has been changed to
      `ready`.
    - The assigned Editor is supposed to check the News item  with status `ready` and if it's acceptable, change
      the News item status to `reviewed`.
    - Once a News item status has been set to `reviewed`, the assigned Writer can no longer access it in the Django
      admin.
    - The assigned Chief Editor would get an e-mail notification about the fact that the News item has been changed
      to `reviewed.`
    - The assigned Chief Editor is supposed to check the News item with status `reviewed` and if it acceptable,
      change the News item status to `published`.
    - Once a News item status has been set to `published`, the assigned Editor can no longer access it in the Django
      admin.
    - Once a News item status has been changed to `published`, all Chief Editors in the system, as well as the
      assigned Writer and Editor get an e-mail notification about the fact that the News item has been published.
    """
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(WerewolfTest, cls).setUpClass()

        # Create groups and test users
        try:
            create_groups_and_test_users(
                chief_editors_group_name = CHIEF_EDITORS_GROUP_NAME,
                editors_group_name = EDITORS_GROUP_NAME,
                writers_group_name = WRITERS_GROUP_NAME
                )
        except Exception as e:
            print(e)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.selenium.quit()
        except Exception as e:
            print(e)

        super(WerewolfTest, cls).tearDownClass()

    @print_info
    def test_01_test_workflow(self):
        """
        Add news item workflow.
        """
        workflow = []

        author = User._default_manager.get(username='writer')
        workflow.append(author)

        editor = User._default_manager.get(username='editor')
        workflow.append(editor)

        chief_editor = User._default_manager.get(username='chief_editor')
        workflow.append(chief_editor)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++ Step 1: Chief editor logs in ++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/news/newsitem/'))
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('chief_editor')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        # Wait until the list view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('changelist')
            )

        # Click the button to add a new news item
        self.selenium.find_element_by_xpath('//a[@class="addlink"]').click()

        # Wait until the add view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('newsitem_form')
            )

        # Filling the form values
        title_input = self.selenium.find_element_by_name("title")
        title_input.send_keys('Lorem ipsum 1')

        slug_input = self.selenium.find_element_by_name("slug")
        slug_input.send_keys('lorem-ipsum-1')

        body_input = self.selenium.find_element_by_name("body")
        if PY3:
            body_input.send_keys(SENTENCES[random.randint(0, len(SENTENCES) - 1)])
        else:
            body_input.send_keys(unicode(SENTENCES[random.randint(0, len(SENTENCES) - 1)]))

        # For chief editor, `author` field is visible and editable
        author_input = self.selenium.find_element_by_xpath(
            '//select[@name="author"]/option[@value="{0}"]'.format(author.pk)
            )
        self.assertTrue(author_input is not None)
        author_input.click()

        # For chief editor, `editor` field is visible and editable
        editor_input = self.selenium.find_element_by_xpath(
            '//select[@name="editor"]/option[@value="{0}"]'.format(editor.pk)
            )
        self.assertTrue(editor_input is not None)
        editor_input.click()

        # For chief editor, `chief_editor` field is visible and editable
        chief_editor_input = self.selenium.find_element_by_xpath(
            '//select[@name="chief_editor"]/option[@value="{0}"]'.format(chief_editor.pk)
            )
        self.assertTrue(chief_editor_input is not None)
        chief_editor_input.click()

        # For chief editor, `status` field has a full list of all available statuses
        for status, label in STATUS_CHOICES:
            status_input = self.selenium.find_element_by_xpath(
                '//select[@name="status"]/option[@value="{0}"]'.format(status)
                )
            self.assertTrue(status_input is not None)

        # Submitting the form (save)
        self.selenium.find_element_by_xpath('//input[@name="_save"]').click()

        # Wait until the list view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('changelist')
            )

        # Check if really is in the list
        news_item = self.selenium.find_element_by_xpath('//a[contains(text(),"Lorem ipsum 1")]')
        news_item_href = news_item.get_attribute('href')

        # Newly inserted news item should be there
        self.assertTrue(news_item is not None)
        workflow.append(news_item_href)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++ Step 2a: Editor logs in ++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as an editor. Accessing /news/newsitem/{news_item.pk}/
        # should be possible. Several fields, such as `chief_editor` shall not be seen/editable.
        # Values of the `status` field are restricted (no `published` option).

        # Trigger the logout
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('editor')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        # Wait until the add view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('newsitem_form')
            )

        # For editor, `author` field is visible and editable
        author_input = self.selenium.find_element_by_xpath(
            '//select[@name="author"]/option[@value="{0}"]'.format(author.pk)
            )
        self.assertTrue(author_input is not None)

        # For editor, `editor` field is not visible/editable
        found = False
        try:
            self.selenium.find_element_by_xpath('//select[@name="editor"]')
            found = True
        except:
            pass

        if found:
            raise Exception("Found form element `editor`, while it's not supposed to be visible/editable.")

        # For editor, `chief_editor` field is not visible/editable
        found = False
        try:
            self.selenium.find_element_by_xpath('//select[@name="chief_editor"]')
            found = True
        except:
            pass

        if found:
            raise Exception("Found form element `chief_editor`, while it's not supposed to be visible/editable.")

        # For editor, `status` field has a restricted list of choices: 'new', 'draft', 'ready', 'reviewed'
        for status in ('new', 'draft', 'ready', 'reviewed'):
            status_input = self.selenium.find_element_by_xpath(
                '//select[@name="status"]/option[@value="{0}"]'.format(status)
                )
            self.assertTrue(status_input is not None)

        # Editor can't set the `status` to 'published', thus 'publish' shouldn't be available in the list
        found = False
        for status in ('published',):
            try:
                self.selenium.find_element_by_xpath(
                    '//select[@name="status"]/option[@value="{0}"]'.format(status)
                    )
                found = True
            except:
                pass

        if found:
            raise Exception("Found `status` value 'published', while it's not supposed to be in the list.")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++ Step 2b: Writer logs in +++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as a writer. Accessing /news/newsitem/{news_item.pk}/
        # should be possible. Several fields, such as `chief_editor` shall not be seen/editable.
        # Values of the `status` field are restricted (no `published` option).

        # Trigger the logout
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('writer')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        # Wait until the add view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('newsitem_form')
            )

        # For writer, `author` field is not visible/editable
        found = False
        try:
            self.selenium.find_element_by_xpath(
                '//select[@name="author"]'
                )
            found = True
        except:
            pass

        if found:
            raise Exception("Found form element `author`, while it's not supposed to be visible/editable.")

        # For writer, `editor` field is not visible/editable
        found = False
        try:
            self.selenium.find_element_by_xpath('//select[@name="editor"]')
            found = True
        except:
            pass

        if found:
            raise Exception("Found form element `editor`, while it's not supposed to be visible/editable.")

        # For writer, `chief_editor` field is not visible/editable
        found = False
        try:
            self.selenium.find_element_by_xpath('//select[@name="chief_editor"]')
            found = True
        except:
            pass

        if found:
            raise Exception("Found form element `chief_editor`, while it's not supposed to be visible/editable.")

        # For writer, `status` field has a restricted list of choices: 'new', 'draft', 'ready'
        for status in ('new', 'draft', 'ready'):
            status_input = self.selenium.find_element_by_xpath(
                '//select[@name="status"]/option[@value="{0}"]'.format(status)
                )
            self.assertTrue(status_input is not None)

        # Writer can't set the `status` to 'reviewed' or 'published'
        found = False
        for status in ('reviewed', 'published',):
            try:
                self.selenium.find_element_by_xpath(
                    '//select[@name="status"]/option[@value="{0}"]'.format(status)
                    )
                found = True
            except:
                pass

        if found:
            raise Exception("Found `status` value 'reviewed' or 'published', "
                            "while it's not supposed to be in the list.")

        # Now the writer sets the status to 'ready'
        status_input = self.selenium.find_element_by_xpath('//select[@name="status"]/option[@value="ready"]')
        self.assertTrue(status_input is not None)
        status_input.click()

        # Submitting the form (save)
        self.selenium.find_element_by_xpath('//input[@name="_save"]').click()

        # Wait until the list view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('changelist')
            )

        # Now log out and login as editor again.

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++ Step 3a: Editor logs in ++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as an editor. Accessing /news/newsitem/{news_item.pk}/
        # should be possible. Several fields, such as `chief_editor` shall not be seen/editable.
        # Values of the `status` field are restricted (no `published` option).

        # Trigger the logout
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('editor')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        # Wait until the add view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('newsitem_form')
            )

        # Now the editor sets the status to 'reviewed'
        status_input = self.selenium.find_element_by_xpath('//select[@name="status"]/option[@value="reviewed"]')
        self.assertTrue(status_input is not None)
        status_input.click()

        # Submitting the form (save)
        self.selenium.find_element_by_xpath('//input[@name="_save"]').click()

        # Wait until the list view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('changelist')
            )

        # Once set to 'reviewed', item shouldn't be visible to writer

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++ Step 3b (fail test): Writer logs in +++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as a writer. Accessing /news/newsitem/{news_item.pk}/
        # should no longer be possible.

        # Trigger the logout
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('writer')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        response = self.client.request()

        try:
            # Wait until the add view opens - this should not work, since 404 page opens
            WebDriverWait(self.selenium, timeout=1).until(
                lambda driver: driver.find_element_by_id('newsitem_form')
                )
        except:
            pass

        # Assuming that 404 raised
        self.assertTrue(404 == response.status_code)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++ Step 4a: Chief editor logs in ++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as an chief editor. Accessing /news/newsitem/{news_item.pk}/
        # should be possible.

        # Logout
        self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/logout/'))
        self.selenium.maximize_window()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('chief_editor')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        # Wait until the add view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('newsitem_form')
            )

        # Now the editor sets the status to 'reviewed'
        status_input = self.selenium.find_element_by_xpath('//select[@name="status"]/option[@value="published"]')
        self.assertTrue(status_input is not None)
        status_input.click()

        # Submitting the form (save)
        self.selenium.find_element_by_xpath('//input[@name="_save"]').click()

        # Wait until the list view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_id('changelist')
            )

        # Once set to 'published', item shouldn't be visible to editor or writer

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++ Step 4b (fail test): Writer logs in +++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as a writer. Accessing /news/newsitem/{news_item.pk}/
        # should no longer be possible.

        # Trigger the logout
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('writer')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        response = self.client.request()

        try:
            # Wait until the add view opens - this should not work, since 404 page opens
            WebDriverWait(self.selenium, timeout=1).until(
                lambda driver: driver.find_element_by_id('newsitem_form')
                )
        except:
            pass

        # Assuming that 404 raised
        self.assertTrue(404 == response.status_code)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++ Step 4c (fail test): Editor logs in ++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Now logging out and logging in as an editor. Accessing /news/newsitem/{news_item.pk}/
        # should no longer be possible.

        # Logout
        self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/logout/'))
        self.selenium.maximize_window()

        # Wait until the login view opens
        WebDriverWait(self.selenium, timeout=4).until(
            lambda driver: driver.find_element_by_xpath('//a[contains(text(),"Log in again")]')
            )

        self.selenium.get(news_item_href)
        self.selenium.maximize_window()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('editor')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        response = self.client.request()

        try:
            # Wait until the add view opens - this should not work, since 404 page opens
            WebDriverWait(self.selenium, timeout=1).until(
                lambda driver: driver.find_element_by_id('newsitem_form')
                )
        except:
            pass

        # Assuming that 404 raised
        self.assertTrue(404 == response.status_code)

        return workflow


if __name__ == "__main__":
    # Tests
    unittest.main()
