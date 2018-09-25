import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import validation as berlin_validators


class Berlin_Dataset_SchemaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config_):
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'berlin_dataset_schema')

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

    def _modify_package_schema(self, schema):
        schema.update({
            'username': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'berlin_type': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'berlin_source': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'date_released': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'date_updated': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'attribution_text': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')                
            ]
        })
        schema.update({
            'temporal_granularity': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'temporal_coverage_from': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'temporal_coverage_to': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'geographical_granularity': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'geographical_coverage': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
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
        return schema

        