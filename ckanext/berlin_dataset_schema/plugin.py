# encoding: utf-8
"""
Module for the CKAN extension defining the dataset schema for daten.berlin.de.
"""

import logging
import os

from ckan.common import _
import ckan.lib.navl.dictization_functions as df
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.berlin_dataset_schema.validation as berlin_validators
from ckanext.berlin_dataset_schema.schema import Schema

log = logging.getLogger(__name__)

class Berlin_Dataset_SchemaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    """
    Main plugin class defining the dataset schema for daten.berlin.de.
    """
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):
        """
        Implementation of IConfigurer.update_config.
        """
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'berlin_dataset_schema')
        site_url = config.get('ckan.site_url', None)
        port = 80
        url_parts = site_url.split(":")
        if len(url_parts) > 2:
            port = url_parts[2]
        config['schema_ref_url'] = f"http://localhost:{port}/terms"

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        schema_path = os.path.join(dir_path, "public", "schema", "berlin_od_schema.json")

        self.json_schema = Schema()
        self.json_schema.load_schema(schema_path)

    # -------------------------------------------------------------------
    # Implementation IDatasetForm
    #
    # Since Berlin_Dataset_SchemaPlugin inherits from DefaultDatasetForm,
    # not all of IDatasetForm's methods need to be implemented here.
    # -------------------------------------------------------------------

    def package_types(self):
        """
        Implementation of IDatasetForm.package_types().

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.package_types
        """
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def is_fallback(self):
        """
        Implementation of IDatasetForm.is_fallback().

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.is_fallback
        """
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def create_package_schema(self):
        """
        Implementation of IDatasetForm.create_package_schema() (the schema for
        creating new packages).

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.create_package_schema
        """
        # let's grab the default schema in our plugin
        schema = super(Berlin_Dataset_SchemaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        """
        Implementation of IDatasetForm.update_package_schema() (the schema for
        updating existing packages).

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.update_package_schema
        """
        # let's grab the default schema in our plugin
        schema = super(Berlin_Dataset_SchemaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def setup_template_variables(self, context, data_dict):
        """
        Implementation of IDatasetForm.setup_template_variables()

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.setup_template_variables
        """
        return {}

    def _get_required_validator(self, attribute):
        """
        For an attribute, return the  matching validator defining requiredness (`not_empty`
        or `ignore_missing`), based on whether or not the loaded JSON schema definies it as
        required.
        """
        if self.json_schema.required(attribute):
            return toolkit.get_validator('not_empty')
        return toolkit.get_validator('ignore_missing')

    def _required_validator_set(self, validator_chain):
        """
        Check if for a chain (list) of validators, the first one
        defines requiredness (`not_empty` or `ignore_missing`)
        """
        if (validator_chain[0] is toolkit.get_validator('not_empty') or
                validator_chain[0] is toolkit.get_validator('ignore_missing')):
            return True
        return False

    def _prepend_required_validator(self, schema):
        """
        Prepend a validator defining requiredness (either `not_empty` or
        `ignore_missing`) to each attribute definition in the schema, but only if:

        - the loaded JSON schema contains the attribute
        - it's not a sub-schema (groups, resources, ...)
        """
        for attribute, validator_chain in schema.items():
            if self.json_schema.contains(attribute):
                attribute_type = self.json_schema.attribute_type(attribute)
                if attribute_type != "array":
                    required_validator = self._get_required_validator(attribute)
                    if not self._required_validator_set(validator_chain):
                        schema[attribute] = [ required_validator ] + validator_chain
                    else:
                        schema[attribute][0] = required_validator
        return schema

    def _modify_package_schema(self, schema):
        """
        Schema for package modifications, used by both create_package_schema and
        update_package_schema.
        """
        # The following are handled by ckan/logic/schema.py/default_create_package_schema():
        # - title
        # - name
        # - author_email
        # - maintainer
        # - url

        schema.update({'berlin_type': [
            toolkit.get_converter('is_berlin_type'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'berlin_source': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'attribution_text': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({
            'url': [
                toolkit.get_converter('is_valid_url')
            ]
        })
        schema.update({'license_id': [
            toolkit.get_converter('is_license_id'),
        ]})
        schema.update({'username': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'date_released': [
            toolkit.get_converter('isodate_notime'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'date_updated': [
            toolkit.get_converter('isodate_notime'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_granularity': [
            toolkit.get_converter('is_temporal_granularity'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_coverage_from': [
            toolkit.get_converter('isodate_notime'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_coverage_to': [
            toolkit.get_converter('isodate_notime'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'geographical_granularity': [
            toolkit.get_converter('is_geo_granularity'),
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'geographical_coverage': [
            toolkit.get_converter('is_geo_feature'),
            toolkit.get_converter('convert_to_extras')
        ]})

        schema = self._prepend_required_validator(schema)

        return schema

    def show_package_schema(self):
        """
        Implementation of IDatasetForm.show_package_schema()

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.show_package_schema
        """

        validator = berlin_validators.Validator()

        # let's grab the default schema in our plugin
        schema = super(Berlin_Dataset_SchemaPlugin, self).show_package_schema()
        schema.update({
            'username': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'berlin_type': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'berlin_source': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'date_released': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_converter('isodate_notime'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'date_updated': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_converter('isodate_notime'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'attribution_text': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_granularity': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_coverage_from': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_converter('isodate_notime'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_coverage_to': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_converter('isodate_notime'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'geographical_granularity': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'geographical_coverage': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        return schema

    def validate(self, context, data_dict, schema, action):
        """
        Implementation of IDatasetForm.validate()

        This is needed to make groups and other non-atomic properties required.

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IDatasetForm.validate
        """
        _errors = {}

        # 'category' would be passed from the package template. If it exists, we generate an entry in
        # 'groups' from it:
        if 'category' in data_dict:
            category = data_dict['category']
            groups = data_dict.get('groups', [])
            data_dict['groups'] = groups + [ { 'name': category } ]

        # The following checks if a user is allowed to edit/create datasets in the given group.
        # TODO: Shouldn't this really be checked elsewhere (authorization)? Validation isn't really
        # the place for it.
        if action != "package_show":
            for group in data_dict.get('groups', []):
                group_name = group.get('name', None)
                validator = berlin_validators.Validator()
                try:
                    validator.is_group_name_valid(group_name, context)
                except df.Invalid as e:
                    _errors['groups'] = _errors.get('groups', []) + [_(f'Group \'{group_name}\' does not exist or cannot be edited by user \'{context["user"]}\'.')]

        (data_dict, errors) = toolkit.navl_validate(data_dict, schema, context)
        if action in [ 'package_create', 'package_update' ]:
            if 'groups' not in data_dict:
                _errors['groups'] = _errors.get('groups', []) + [ _('Required field \'groups\' not set.') ]

        if 'groups' in _errors:
            errors['groups'] = errors.get('groups', []) + _errors['groups']

        return (data_dict, errors)

    # -------------------------------------------------------------------
    # Implementation IValidators
    # -------------------------------------------------------------------

    def get_validators(self):
        """
        Implementation of IValidators.get_validators()

        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IValidators.get_validators
        """
        validator = berlin_validators.Validator()

        return {
            "isodate_notime": validator.isodate_notime ,
            "is_valid_url": validator.is_valid_url ,
            "is_berlin_type": validator.is_berlin_type ,
            "is_license_id": validator.is_license_id ,
            "is_geo_feature": validator.is_geo_feature ,
            "is_geo_granularity": validator.is_geo_granularity ,
            "is_temporal_granularity": validator.is_temporal_granularity ,
            "is_group_name_valid": validator.is_group_name_valid
        }
