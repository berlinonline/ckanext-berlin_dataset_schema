# coding: utf-8
"""
Custom validation functions for the extended version of the CKAN
package schema.
"""

import logging
from datetime import datetime
import os
import validators

from ckan.common import _
import ckan.logic as logic
from ckan.logic.validators import boolean_validator
import ckan.model as model
from ckan.plugins.toolkit import asbool
from ckan.common import c
import ckan.lib.navl.dictization_functions as df

from ckanext.berlin_dataset_schema.schema import Schema

LOG = logging.getLogger(__name__)
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

    def license_ids(self):
        """
        Return the currently valid values of 'license_id'.
        """
        enum = self.json_schema.enum_for_attribute('license_id')
        return enum

    def geo_features(self):
        """
        Return the currently valid values of 'geographical_coverage'.
        """
        enum = self.json_schema.enum_for_attribute('geographical_coverage')
        return enum

    def geo_granularities(self):
        """
        Return the currently valid values of 'geographical_granularity'.
        """
        enum = self.json_schema.enum_for_attribute('geographical_granularity')
        return enum

    def temporal_granularities(self):
        """
        Return the currently valid values of 'temporal_granularity'.
        """
        enum = self.json_schema.enum_for_attribute('temporal_granularity')
        return enum

    def sample_records(self) -> list:
        '''
        Return the currently valid values of the 'sample_record' metadatum.
        '''
        enum = self.json_schema.enum_for_attribute('sample_record')
        return enum
    
    def hvd_categories(self) -> list:
        '''
        Return the currently valid values of the 'hvd_category' metadatum.
        '''
        enum = self.json_schema.enum_for_attribute('hvd_category')
        return enum
    
    def isodate_notime(self, value):
        """
        Validator function to check that a value corresponds to the
        ISO8601 pattern YYYY-MM-DD.

        Valid datetimes that extend beyond that pattern will be 
        shortened to YYYY-MM-DD, empty values will be transformed to None.

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
            raise df.Invalid(_('Date format incorrect. Use ISO8601: YYYY-MM-DD.'))
        return date

    def is_valid_url(self, value):
        if value: # None, emtpy string is also valid
            if not validators.url(value):
                raise df.Invalid(_(f'URL seems to be invalid: "{value}"'))
        return value

    def is_in_enum(self, value, value_space):
        """
        Helper that checks if `value` is contained in `value_space`.
        Returns `value` if it is contained, raises Exception if not.
        """
        if isinstance(value_space, list):
            if value in value_space:
                return value
            else:
                quoted = [f'\'{x.encode("utf-8")}\'' for x in value_space]
                message = f'\'{value}\' is not one of [ {", ".join(quoted)} ].'
                raise df.Invalid(_(message))
        raise df.Invalid('\'value_space\' must be a list.')

    def is_berlin_type(self, value):
        """
        Validator function to check that a value is one of ['datensatz', 'dokument', 'app'].
        """
        value_space = self.berlin_types()
        return self.is_in_enum(value, value_space)

    def is_license_id(self, value):
        """
        Validator function to check that a value is one of the currently available license ids.
        """
        value_space = self.license_ids()
        return self.is_in_enum(value, value_space)

    def is_geo_feature(self, value):
        """
        Validator function to check that a value is one of the currently available
        values for geographical coverage.
        """
        value_space = self.geo_features()
        return self.is_in_enum(value, value_space)

    def is_geo_granularity(self, value):
        """
        Validator function to check that a value is one of the currently available
        values for geographical granularity.
        """
        value_space = self.geo_granularities()
        return self.is_in_enum(value, value_space)

    def is_temporal_granularity(self, value):
        """
        Validator function to check that a value is one of the currently available
        values for temporal granularity.
        """
        value_space = self.temporal_granularities()
        return self.is_in_enum(value, value_space)

    def is_sample_record(self, value: str):
        '''
        Validator function to check that a value is one of the currently available
        values for the metadatum 'sample_record'.
        '''
        value_space = self.sample_records()
        return self.is_in_enum(value, value_space)
        
    def is_hvd_category(self, value: str):
        '''
        Validator function to check that a value is one of the currently available
        values for the metadatum 'hvd_category'.
        '''
        value_space = self.hvd_categories()
        return self.is_in_enum(value, value_space)
        
    def is_group_name_valid(self, name, context):
        """
        Check if a name is a valid group name for the current user (i.e., the user is authorized to
        add packages to this group).

        Returns name if valid, raises df.Invalid if not.
        """
        context['is_member'] = True

        users_groups = get_action('group_list_authz')(context, {})
        group_names = [ group['name'] for group in users_groups ]
        if name in group_names:
            return name
        else:
            raise df.Invalid(_(f'Group \'{name}\' does not exist or cannot be edited by user \'{context["user"]}\'.'))

    def is_booleanish(self, value: bool) -> bool:
        """
        Checks if `value` is a true boolean or one of `['true', 'false']`.
        Returns `True|False` if valid, raises df.Invalid if not.

        ckan.logic.validators.boolean_validator() doesn't help, because it converts all kinds of
        true-ish values, never raises an error and crashes if value does not have lower().
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            if value.lower() == 'false':
                return False

        raise df.Invalid(_(f"{value} is not a boolean, and not one of ['true', 'false']."))

    def boolean_converter(self, value) -> bool:
        """
        Use `boolean_validator` for conversion of bool to/from string (needed
        for extras, which are always saved as strings), but handle potential
        AttributeErrors.
        """
        try:
            return boolean_validator(value, None)
        except AttributeError as e:
            # boolean_validator tries to call lower() on `value`, which in
            # some cases (`None`, int values etc.) leads to an AttributeError.
            # We need to handle that.
            raise df.Invalid(str(e))

    def personal_data_settings_valid(self, key, data, errors, context):
        """
        Check if the interplay of `personal_data`, `personal_data_exemption` and `data_anonymized`
        is correct.
        """

        def _asbool(key, data, errors):
            converted = False
            try:
                converted = asbool(data.get(key, False))
            except ValueError as e:
                errors[key].append(e)
            return converted

        personal_data = _asbool(('personal_data',), data, errors)
        personal_data_exemption = _asbool(('personal_data_exemption',), data, errors)
        data_anonymized = _asbool(('data_anonymized',), data, errors)

        if not personal_data:
            if personal_data_exemption:
                errors[('personal_data_exemption',)].append(_("Daten ohne Personenbezug können keiner Sonderregelung unterliegen."))
            if data_anonymized:
                errors[('data_anonymized',)].append(_("Daten ohne Personenbezug können nicht anonymisiert werden."))
        else:
            if personal_data_exemption:
                if data_anonymized:
                    errors[('data_anonymized',)].append(_("Wenn Daten mit Personenbezug einer Sonderregelung unterliegen, sollten sie nicht anonymisiert werden."))
            else:
                if not data_anonymized:
                    errors[('personal_data_exemption',)].append(_("Daten mit Personenbezug müssen entweder einer Sonderregelung unterliegen, oder vor der Veröffentlichung anonymisiert werden."))
                    errors[('data_anonymized',)].append(_("Daten mit Personenbezug müssen entweder einer Sonderregelung unterliegen, oder vor der Veröffentlichung anonymisiert werden."))

