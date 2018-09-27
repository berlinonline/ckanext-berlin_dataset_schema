import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.berlin_dataset_schema.validation as berlin_validators
from ckanext.berlin_dataset_schema.schema import Schema

from pprint import pformat

log = logging.getLogger(__name__)


class Berlin_Dataset_SchemaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'berlin_dataset_schema')
        site_url = config.get('ckan.site_url', None)
        port = 80
        url_parts = site_url.split(":")
        if len(url_parts) > 2:
            port = url_parts[2]
        config['schema_ref_url'] = "http://localhost:{}{}".format(port, "/terms")
        self.json_schema = Schema()
        self.json_schema.load_schema()

    # -------------------------------------------------------------------
    # Implementation IDatasetForm
    # -------------------------------------------------------------------
    
    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(Berlin_Dataset_SchemaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(Berlin_Dataset_SchemaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema
    
    def setup_template_variables(self, context, data_dict):
        return {}

    def _get_required_validator(self, attribute):
        if self.json_schema.required(attribute):
            return toolkit.get_validator('not_empty')
        return toolkit.get_validator('ignore_missing')

    def _required_validator_set(self, validator_chain):
        if (validator_chain[0] is toolkit.get_validator('not_empty') or
                validator_chain[0] is toolkit.get_validator('ignore_missing')):
            return True
        return False

    def _prepend_required_validator(self, schema):
        for attribute, validator_chain in schema.iteritems():
            log.debug(attribute)
            if self.json_schema.contains(attribute):
                attribute_type = self.json_schema.attribute_type(attribute)
                log.debug("\t%s", attribute_type)
                if attribute_type != "array":
                    required_validator = self._get_required_validator(attribute)
                    if not self._required_validator_set(validator_chain):
                        log.debug("required-validator not set")
                        schema[attribute] = [ required_validator ] + validator_chain
                    else:
                        schema[attribute][0] = required_validator
        return schema

    def _modify_package_schema(self, schema):
        # The following are handled by ckan/logic/schema.py/default_create_package_schema():
        # - title
        # - name
        # - author_email
        # - maintainer
        # - url

        schema.update({'berlin_type': [
            berlin_validators.is_berlin_type,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'berlin_source': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'attribution_text': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'username': [
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'date_released': [
            berlin_validators.isodate_notime,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'date_updated': [
            berlin_validators.isodate_notime,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_granularity': [
            # TODO: add validation
            # berlin_validators.contained_in_enum,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_coverage_from': [
            berlin_validators.isodate_notime,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'temporal_coverage_to': [
            berlin_validators.isodate_notime,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'geographical_granularity': [
            # TODO: add validation
            # berlin_validators.contained_in_enum,
            toolkit.get_converter('convert_to_extras')
        ]})
        schema.update({'geographical_coverage': [
            # TODO: add validation
            # berlin_validators.contained_in_enum,
            toolkit.get_converter('convert_to_extras')
        ]})

        log.debug(pformat(schema))
        schema = self._prepend_required_validator(schema)
        log.debug(pformat(schema))

        return schema

    def show_package_schema(self):
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
                berlin_validators.isodate_notime,
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'date_updated': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
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
                berlin_validators.isodate_notime,
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_coverage_to': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
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
