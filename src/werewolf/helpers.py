__title__ = 'werewolf.helpers'
__version__ = '0.3'
__build__ = 0x000003
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('admin_edit_url', 'admin_edit_url_for_object')

from django.core.urlresolvers import reverse

def admin_edit_url(app_label, module_name, object_id, url_title=None):
    """
    Gets an admin edit URL for the object given.

    :param str app_label:
    :param str module_name:
    :param int object_id:
    :param str url_title: If given, an HTML a tag is returned with `url_title` as the tag title. If left to None
        just the URL string is returned.
    :return str:
    """
    try:
        url = reverse('admin:%s_%s_change' %(app_label, module_name), args=[object_id])
        if url_title:
            return u'<a href="%s">%s</a>' %(url, url_title)
        else:
            return url
    except:
        return None

def admin_edit_url_for_object(obj, url_title=None):
    """
    Gets an admin edit URL for the object given.

    :param django.db.models.Model obj: Django model subclass.
    :param str url_title: If given, an HTML a tag is returned with `url_title` as the tag title. If left to None
        just the URL string is returned.
    :return str:
    """
    return admin_edit_url(obj._meta.app_label, obj._meta.module_name, obj.id, url_title)
