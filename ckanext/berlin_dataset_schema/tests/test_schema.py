# coding: utf-8
"""Tests for schema.py."""

import logging
import os

from nose.tools import with_setup
from nose.tools import raises

import ckan.plugins as plugins
import ckanext.berlin_dataset_schema.schema as schema

log = logging.getLogger(__name__)
PLUGIN_NAME = 'berlin_dataset_schema'

# class TestCompleteSchema(object):

#     @classmethod
#     def setup_class(cls):
#         plugins.load(PLUGIN_NAME)

#     @classmethod
#     def teardown_class(cls):
#         plugins.unload(PLUGIN_NAME)

#     def setup(self):
#         path = os.path.abspath(__file__)
#         dir_path = os.path.dirname(path)
#         schema_path = os.path.join(dir_path, "resources", "berlin_od_schema.json")
#         schema.Schema().load_schema(schema_path)

#     def teardown(self):
#         schema.Schema().unload_schema()

#     def test_author_property_is_required(self):
#         assert schema.Schema().required('author') is True

#     def test_maintainer_property_is_not_required(self):
#         assert schema.Schema().required('maintainer') is False

#     def test_schema_contains_group_property(self):
#         assert schema.Schema().contains('groups') is True

#     def test_schema_does_not_contain_id_property(self):
#         assert schema.Schema().contains('id') is False

#     def test_geographical_granularity_property_has_type_string(self):
#         assert schema.Schema().attribute_type('geographical_granularity') == 'string'

#     def test_groups_property_has_type_array(self):
#         assert schema.Schema().attribute_type('groups') == 'array'

#     def test_non_existant_property_has_type_none(self):
#         assert schema.Schema().attribute_type('foo_bar') is None

#     def test_enum_for_attribute_returns_correct_list(self):
#         expected_list = [ 'datensatz', 'dokument', 'app' ]
#         assert schema.Schema().enum_for_attribute('berlin_type').sort() is expected_list.sort()

#     def test_enum_for_attribute_returns_none_for_unenumerated(self):
#         assert schema.Schema().enum_for_attribute('author') is None

#     def test_attribute_definition_for_existing_attribute_is_dict(self):
#         definition = schema.Schema().attribute_definition('geographical_coverage')
#         assert isinstance(definition, dict)
    
#     def test_attribute_definition_for_missing_attribute_is_none(self):
#         assert schema.Schema().attribute_definition('foo') is None
    
#     @raises(schema.SchemaError)
#     def test_enum_for_attribute_raises_error_for_undefined_attribute(self):
#         schema.Schema().enum_for_attribute('foo_bar')


class TestEmptySchema(object):

    @classmethod
    def setup_class(cls):
        plugins.load(PLUGIN_NAME)

    @classmethod
    def teardown_class(cls):
        plugins.unload(PLUGIN_NAME)

    def setup(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        schema_path = os.path.join(dir_path, "resources", "berlin_od_schema_empty.json")
        schema.Schema().load_schema(schema_path)
        assert schema.Schema().schema == { "foo": "bar" }
        # assert len(schema.Schema().schema.keys()) == 0

    def teardown(self):
        schema.Schema().unload_schema()

    @raises(schema.SchemaError)
    def test_empty_schema_raises_schema_error_on_enum_for_attribute(self):
        schema.Schema().enum_for_attribute('author')

    @raises(schema.SchemaError)
    def test_empty_schema_raises_schema_error_on_attribute_type(self):
        schema.Schema().attribute_type('author')

    @raises(schema.SchemaError)
    def test_empty_schema_raises_schema_error_on_contains(self):
        schema.Schema().contains('author')

    @raises(schema.SchemaError)
    def test_empty_schema_raises_schema_error_on_required(self):
        schema.Schema().required('author')

    @raises(schema.SchemaError)
    def test_empty_schema_raises_schema_error_on_attribute_definition(self):
        schema.Schema().attribute_definition('author')

# class TestNoSchemaLoaded(object):

#     @classmethod
#     def setup_class(cls):
#         plugins.load(PLUGIN_NAME)
#         schema.Schema().unload_schema()

#     @classmethod
#     def teardown_class(cls):
#         plugins.unload(PLUGIN_NAME)

#     @raises(schema.SchemaError)
#     def test_accessing_schema_without_loading_raises_attribute_error(self):
#         log.debug(schema.Schema().schema())
#         schema.Schema().required('author')
    