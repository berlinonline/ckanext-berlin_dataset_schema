# coding: utf-8
"""
Custom validation functions for the extended version of the CKAN
package schema.
"""

import logging
from datetime import datetime
import os
from ckan.common import _
import ckan.logic as logic
import ckan.model as model
from ckan.common import c
import ckan.lib.navl.dictization_functions as df

from ckanext.berlin_dataset_schema.schema import Schema

log = logging.getLogger(__name__)
get_action = logic.get_action

class Validator(object):
    
    def __init__(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        schema_path = os.path.join(dir_path, "public", "schema", "berlin_od_schema.json")

        self.json_schema = Schema()
        self.json_schema.load_schema(schema_path)


    def berlin_types(self):
        """
        Return the currently valid values of 'berlin_type'.
        """
        enum = self.json_schema.enum_for_attribute('berlin_type')
        return enum

    def isodate_notime(self, value):
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
            raise df.Invalid(_('Date format incorrect. Use ISO8601: YYYY-MM-DD. Only ' + \
            'dates after 1900 allowed!'))
        return date

    def is_in_enum(self, value, value_space):
        """
        Helper that checks if `value` is contained in `value_space`.
        Returns `value` if it is contained, raises `Invalid` error if not.
        """
        if isinstance(value_space, list):
            if value in value_space:
                return value
            else:
                raise df.Invalid(
                    _('`{}` is not one of [ {} ].'.format(value, ', '.join(value_space))))
        raise Exception('`value_space` must be a list.')

    def is_berlin_type(self, value):
        """
        Validator function to check that a value is one of ['datensatz', 'dokument', 'app'].
        """
        value_space = self.berlin_types()
        return self.is_in_enum(value, value_space)

    def is_group_name_valid(self, name, context):
        """
        Check if a name is a valid group name for the current user (i.e., the user is authorized to
        add packages to this group).
        """
        context['is_member'] = True

        users_groups = get_action('group_list_authz')(context, {})
        group_names = [ group['name'] for group in users_groups ]
        if name in group_names:
            return True
        return False
