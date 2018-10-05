# coding: utf-8
"""
Custom validation functions for the extended version of the CKAN
package schema.
"""

import logging
from datetime import datetime
from ckan.common import _
import ckan.logic as logic
import ckan.model as model
from ckan.common import c
import ckan.lib.navl.dictization_functions as df

log = logging.getLogger(__name__)
get_action = logic.get_action

def berlin_types():
    """
    Return the currently valid values of 'berlin_type'.
    """
    return [
        u'datensatz' ,
        u'dokument' ,
        u'app'
    ]

def isodate_notime(value):
    """
    Validator function to check that a value corresponds to the
    ISO8601 pattern YYYY-MM-DD.

    Valid datetimes that extend beyond that pattern will be 
    shortened to YYYY-MM-DD, empty values will be transformed to None.

    Due to limitations of earlier versions of Python, dates past 
    1900 will cause an Exception.

    value -- the date value to be validated
    """
    if isinstance(value, datetime):
        return value.__format__("%Y-%m-%d")
    if value == '':
        return None
    try:
        date = datetime.strptime(value[:10], "%Y-%m-%d")
        date = date.__format__("%Y-%m-%d")
    except (TypeError, ValueError):
        raise df.Invalid(_('Date format incorrect. Use ISO8601: YYYY-MM-DD. Only \
        dates after 1900 allowed!'))
    return date

def is_berlin_type(value):
    """
    Validator function to check that a value is one of ['datensatz', 'dokument', 'app'].
    """
    _berlin_types = berlin_types()
    if value in _berlin_types:
        return value
    else:
        raise df.Invalid(_('berlin_type must be one of [ {} ].'.format(', '.join(_berlin_types))))

def is_group_name_valid(name, context=None):
    """
    Check if a name is a valid group name for the current user.
    """
    if not context:
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user,
            'auth_user_obj': c.userobj,
            'use_cache': False
        }
    context['is_member'] = True

    users_groups = get_action('group_list_authz')(context, {})
    group_names = [ group['name'] for group in users_groups ]
    if name in group_names:
        return True
    return False
